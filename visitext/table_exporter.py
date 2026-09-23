import csv
import io
import re
from typing import List


class TableExporter:
    """Parses reconstructed document lines into structured columns and exports to CSV and Markdown."""

    def __init__(self, delimiter_pattern: str = r'\s{2,}|\t+|\|'):
        self.delimiter_pattern = delimiter_pattern

    def parse_lines_to_rows(self, lines: List[str]) -> List[List[str]]:
        rows: List[List[str]] = []
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue

            # Split line into columns based on multiple spaces, tabs, or pipe symbols
            cells = [c.strip() for c in re.split(self.delimiter_pattern, line_clean) if c.strip()]
            if cells:
                rows.append(cells)
        return rows

    def to_csv(self, rows: List[List[str]]) -> str:
        if not rows:
            return ""
        output = io.StringIO()
        writer = csv.writer(output, lineterminator='\n')
        for row in rows:
            writer.writerow(row)
        return output.getvalue()

    def to_markdown(self, rows: List[List[str]]) -> str:
        if not rows:
            return ""

        max_cols = max(len(r) for r in rows)
        # Normalize row lengths
        padded_rows = [r + [""] * (max_cols - len(r)) for r in rows]

        # Calculate max width for each column
        col_widths = [
            max(len(padded_rows[row_idx][col_idx]) for row_idx in range(len(padded_rows)))
            for col_idx in range(max_cols)
        ]
        # Enforce minimum width of 3 for markdown separators
        col_widths = [max(w, 3) for w in col_widths]

        md_lines = []

        # Header
        header_cells = [
            padded_rows[0][i].ljust(col_widths[i])
            for i in range(max_cols)
        ]
        md_lines.append("| " + " | ".join(header_cells) + " |")

        # Separator
        separators = ["-" * w for w in col_widths]
        md_lines.append("| " + " | ".join(separators) + " |")

        # Data rows
        for row in padded_rows[1:]:
            cells = [
                row[i].ljust(col_widths[i])
                for i in range(max_cols)
            ]
            md_lines.append("| " + " | ".join(cells) + " |")

        return "\n".join(md_lines)