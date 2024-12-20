import logging
import re
from pathlib import Path
from typing import List, Union

import sqlglot
from sqlglot.expressions import Create, Select

from .models import SQLDependency
from .parsers.column_parser import ColumnParser
from .parsers.table_parser import TableParser


class SQLDependencyExtractor:
    """Extracts table and column dependencies from SQL queries."""

    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _extract_statements(self, sql: str) -> List[str]:
        """Extract all relevant SQL statements from function body."""
        # Extract function body if this is a function
        function_body_match = re.search(
            r"\$(?:function|[^\$]*)\$(.*?)\$(?:function|[^\$]*)\$", sql, re.DOTALL
        )
        if function_body_match:
            sql = function_body_match.group(1)

        statements = []

        # Extract CREATE TABLE AS SELECT statements
        creates = re.finditer(
            r"CREATE (?:TEMPORARY )?TABLE.*?AS\s+SELECT.*?;",
            sql,
            re.DOTALL | re.IGNORECASE,
        )
        for match in creates:
            statements.append(match.group(0))

        # Extract RETURN QUERY SELECT statement if it exists
        return_query = re.search(
            r"RETURN QUERY\s+(SELECT.*?);(?:\s*END)?", sql, re.DOTALL | re.IGNORECASE
        )
        if return_query:
            statements.append(return_query.group(1))

        # If no statements found, return original SQL
        return statements if statements else [sql]

    def _merge_dependencies(self, deps: List[SQLDependency]) -> SQLDependency:
        """Merge multiple SQLDependency objects into one."""
        all_tables = set()
        all_columns = {}

        for dep in deps:
            all_tables.update(dep.tables)
            for table, columns in dep.columns.items():
                if table not in all_columns:
                    all_columns[table] = set()
                all_columns[table].update(columns)

        return SQLDependency(
            tables=all_tables,
            columns=all_columns,
            query="",  # Empty since this is a merged result
        )

    def extract_from_query(self, sql: str) -> SQLDependency:
        """Extract dependencies from a single SQL query."""
        all_dependencies = []

        try:
            # Extract all relevant statements
            statements = self._extract_statements(sql)

            # Process each statement
            for stmt in statements:
                try:
                    # Parse the SQL
                    expression = sqlglot.parse_one(stmt)

                    # If it's a CREATE TABLE AS SELECT, focus on the SELECT part
                    if isinstance(expression, Create) and expression.find(Select):
                        select_part = expression.find(Select)
                        tables = TableParser.extract_tables(select_part)
                        # Add the created table
                        created_table = (
                            f"{expression.this.db}.{expression.this.name}"
                            if expression.this.db
                            else expression.this.name
                        )
                        tables.add(created_table)
                        columns = ColumnParser.extract_columns(select_part)
                    else:
                        tables = TableParser.extract_tables(expression)
                        columns = ColumnParser.extract_columns(expression)

                    all_dependencies.append(
                        SQLDependency(tables=tables, columns=columns, query=stmt)
                    )
                except Exception as e:
                    self.logger.error(f"Error processing statement: {str(e)}")

            # Merge all dependencies
            if all_dependencies:
                return self._merge_dependencies(all_dependencies)

        except Exception as e:
            self.logger.error(f"Error extracting dependencies: {str(e)}")

        # Return empty result if nothing found
        return SQLDependency(tables=set(), columns={}, query=sql)

    def extract_from_file(self, file_path: Union[str, Path]) -> List[SQLDependency]:
        """Extract dependencies from SQL statements in a file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")

        try:
            with open(file_path, "r") as f:
                sql_script = f.read()

            return self.extract_from_script(sql_script)
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def extract_from_script(self, sql_script: str) -> List[SQLDependency]:
        """Extract dependencies from multiple SQL statements in a script."""
        dependency = self.extract_from_query(sql_script)
        return [dependency] if dependency.tables else []
