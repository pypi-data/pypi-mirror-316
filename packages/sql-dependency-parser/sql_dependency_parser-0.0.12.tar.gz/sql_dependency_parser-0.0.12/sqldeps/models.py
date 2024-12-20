from dataclasses import dataclass
from typing import Dict, Set
import json

@dataclass
class SQLDependency:
    """Data class to hold dependency information."""
    
    tables: Set[str]
    columns: Dict[str, Set[str]]  # table -> columns mapping
    query: str

    def __repr__(self) -> str:
        return f"SQLDependency(tables={self.tables}, columns={self.columns})"

    def _repr_html_(self) -> str:
        """HTML representation for Jupyter notebooks."""
        html = ["<div style='font-family: monospace;'>"]
        html.append("<h3>SQL Dependencies</h3>")
        
        if self.tables:
            html.append("<h4>Tables:</h4>")
            html.append("<ul style='margin-top: 0'>")
            for table in sorted(self.tables):
                html.append(f"<li>{table}</li>")
            html.append("</ul>")
        
        if self.columns:
            html.append("<h4>Columns by Table:</h4>")
            html.append("<ul style='margin-top: 0'>")
            for table in sorted(self.columns.keys()):
                cols = sorted(self.columns[table])
                html.append(f"<li><strong>{table}</strong>")
                html.append("<ul>")
                for col in cols:
                    html.append(f"<li>{col}</li>")
                html.append("</ul></li>")
            html.append("</ul>")
        
        html.append("</div>")
        return "\n".join(html)

    def to_dict(self) -> Dict:
        """Convert to a dictionary format with sorted values."""
        return {
            "tables": sorted(list(self.tables)),
            "columns": {
                table: sorted(list(columns))
                for table, columns in sorted(self.columns.items())
            }
        }
