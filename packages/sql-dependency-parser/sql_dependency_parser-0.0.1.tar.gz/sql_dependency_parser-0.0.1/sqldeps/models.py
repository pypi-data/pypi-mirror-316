from dataclasses import dataclass
from typing import Dict, Set


@dataclass
class SQLDependency:
    """Data class to hold dependency information."""

    tables: Set[str]
    columns: Dict[str, Set[str]]  # table -> columns mapping
    query: str

    def __repr__(self) -> str:
        return f"SQLDependency(tables={self.tables}, columns={self.columns})"
