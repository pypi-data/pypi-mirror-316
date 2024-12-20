import logging
import re
from pathlib import Path
from typing import List, Set, Union

import sqlglot
from sqlglot.expressions import Create, Select, Table

from .models import SQLDependency
from .parsers.column_parser import ColumnParser
from .parsers.table_parser import TableParser

class PostgreSQLFilter(logging.Filter):
    """Filter out PostgreSQL-specific syntax warnings."""
    
    def filter(self, record):
        # Skip PostgreSQL-specific command warnings
        postgres_commands = [
            "ANALYZE",
            "VACUUM",
            "CLUSTER",
            "REINDEX",
            "LISTEN",
            "NOTIFY",
            "REFRESH"
        ]
        
        # Create the pattern like: "'.*(ANALYZE|VACUUM|etc).*'"
        pattern = f"'.*({('|'.join(postgres_commands))}).*'"
        
        # Skip if the message contains PostgreSQL-specific commands
        if record.msg.startswith(pattern):
            return False
            
        # Skip generic sqlglot warnings about unsupported syntax
        if "contains unsupported syntax" in record.msg:
            return False
            
        # Skip other known sqlglot parsing warnings
        if "Invalid expression / Unexpected token" in record.msg:
            return False
            
        # Allow all other messages
        return True


class SQLDependencyExtractor:
    """Extracts table and column dependencies from SQL queries."""

    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            # Add the PostgreSQL-specific filter
            handler.addFilter(PostgreSQLFilter())
            self.logger.addHandler(handler)

    def _extract_statements(self, sql: str) -> List[str]:
        """Extract all relevant SQL statements from both function bodies and standalone SQL."""
        statements = []
        
        # First find all function definitions
        function_matches = list(re.finditer(
            r"\$(?:function|[^\$]*)\$(.*?)\$(?:function|[^\$]*)\$",
            sql,
            re.DOTALL
        ))
        
        if function_matches:
            # Process each function body
            for match in function_matches:
                function_body = match.group(1)
                # Extract CREATE TABLE AS SELECT statements from function
                creates = re.finditer(
                    r"CREATE (?:TEMPORARY )?TABLE.*?AS\s+SELECT.*?;",
                    function_body,
                    re.DOTALL | re.IGNORECASE,
                )
                for create_match in creates:
                    statements.append(create_match.group(0))

                # Extract RETURN QUERY SELECT statements from function
                return_query = re.search(
                    r"RETURN QUERY\s+(SELECT.*?);(?:\s*END)?",
                    function_body,
                    re.DOTALL | re.IGNORECASE
                )
                if return_query:
                    statements.append(return_query.group(1))
                    
            # Now get the SQL outside of functions
            last_end = 0
            non_function_parts = []
            
            for match in function_matches:
                # Add the part before this function
                if match.start() > last_end:
                    non_function_parts.append(sql[last_end:match.start()])
                last_end = match.end()
            
            # Add any remaining SQL after the last function
            if last_end < len(sql):
                non_function_parts.append(sql[last_end:])
                
            # Process non-function parts
            for part in non_function_parts:
                # Split by semicolon and filter out empty statements
                stmt_list = [s.strip() for s in part.split(';') if s.strip()]
                statements.extend(stmt_list)
        else:
            # If no functions found, treat entire SQL as standalone statements
            statements = [s.strip() for s in sql.split(';') if s.strip()]
        
        # If no statements found at all, return original SQL
        return statements if statements else [sql]

    def _is_temporary_table(self, create_stmt: str) -> bool:
        """Check if a CREATE TABLE statement is for a temporary table."""
        return bool(re.search(r"CREATE\s+TEMPORARY\s+TABLE", create_stmt, re.IGNORECASE))

    def _merge_dependencies(self, deps: List[SQLDependency], original_query: str) -> SQLDependency:
        """Merge multiple SQLDependency objects into one."""
        all_tables = set()
        all_columns = {}
        temp_tables = set()

        # First pass: identify temporary tables
        for stmt in self._extract_statements(original_query):
            if self._is_temporary_table(stmt):
                match = re.search(r"CREATE\s+TEMPORARY\s+TABLE\s+(\w+)", stmt, re.IGNORECASE)
                if match:
                    temp_tables.add(match.group(1))

        # Second pass: merge dependencies
        for dep in deps:
            # Add all non-temporary tables
            tables_to_add = dep.tables - temp_tables
            all_tables.update(tables_to_add)
            
            # Add columns from non-temporary tables
            for table, columns in dep.columns.items():
                if table not in temp_tables:
                    if table not in all_columns:
                        all_columns[table] = set()
                    all_columns[table].update(columns)

        return SQLDependency(
            tables=all_tables,
            columns=all_columns,
            query=original_query
        )

    def extract_from_query(self, sql: str) -> SQLDependency:
        """Extract dependencies from a single SQL query."""
        all_dependencies = []
        temp_tables = set()

        try:
            # Extract all relevant statements
            statements = self._extract_statements(sql)

            # First pass: identify temporary tables
            for stmt in statements:
                if self._is_temporary_table(stmt):
                    match = re.search(r"CREATE\s+TEMPORARY\s+TABLE\s+(\w+)", stmt, re.IGNORECASE)
                    if match:
                        temp_tables.add(match.group(1))

            # Process each statement
            for stmt in statements:
                try:
                    # Parse the SQL
                    expression = sqlglot.parse_one(stmt)

                    # If it's a CREATE TABLE AS SELECT, focus on the SELECT part
                    if isinstance(expression, Create) and expression.find(Select):
                        select_part = expression.find(Select)
                        tables = TableParser.extract_tables(select_part)
                        
                        # Only add the created table if it's not temporary
                        if not self._is_temporary_table(stmt):
                            created_table = (
                                f"{expression.this.db}.{expression.this.name}"
                                if expression.this.db
                                else expression.this.name
                            )
                            tables.add(created_table)
                            
                        columns = ColumnParser.extract_columns(select_part)
                    else:
                        # For regular SELECT statements, filter out temporary tables
                        tables = {t for t in TableParser.extract_tables(expression) 
                                if t not in temp_tables}
                        columns = ColumnParser.extract_columns(expression)

                    all_dependencies.append(
                        SQLDependency(tables=tables, columns=columns, query=stmt)
                    )
                except Exception as e:
                    self.logger.error(f"Error processing statement: {str(e)}")

            # Merge all dependencies
            if all_dependencies:
                return self._merge_dependencies(all_dependencies, sql)

        except Exception as e:
            self.logger.error(f"Error extracting dependencies: {str(e)}")

        # Return empty result if nothing found
        return SQLDependency(tables=set(), columns={}, query=sql)

    def extract_from_file(self, file_path: Union[str, Path]) -> SQLDependency:
        """Extract dependencies from SQL statements in a file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")

        try:
            with open(file_path, "r") as f:
                sql_script = f.read()

            # Extract dependencies directly
            return self.extract_from_query(sql_script)

        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def extract_from_script(self, sql_script: str) -> SQLDependency:
        """Extract dependencies from multiple SQL statements in a script."""
        return self.extract_from_query(sql_script)
