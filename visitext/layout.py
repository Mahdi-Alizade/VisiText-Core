from typing import List
from visitext.models import TextBlock


class TextLine:
    """Represents a grouped single line of text assembled from spatial blocks."""

    def __init__(self, y_reference: int, tolerance: int = 10):
        self.y_reference = y_reference
        self.tolerance = tolerance
        self.blocks: List[TextBlock] = []

    def can_include(self, block: TextBlock) -> bool:
        if not block.bbox:
            return False
        return abs(block.bbox.y - self.y_reference) <= self.tolerance

    def add_block(self, block: TextBlock) -> None:
        self.blocks.append(block)

    def get_sorted_text(self) -> str:
        # Sort words along the X-axis from left to right
        sorted_blocks = sorted(
            self.blocks,
            key=lambda b: b.bbox.x if b.bbox else 0
        )
        return " ".join([b.text for b in sorted_blocks])


class LayoutReconstructor:
    """Reassembles flat token streams into ordered physical document lines."""

    def __init__(self, vertical_tolerance: int = 12):
        self.vertical_tolerance = vertical_tolerance

    def reconstruct_lines(self, blocks: List[TextBlock]) -> List[str]:
        valid_blocks = [b for b in blocks if b.bbox is not None]
        if not valid_blocks:
            return []

        # Sort all blocks primarily by Y-coordinate
        sorted_by_y = sorted(valid_blocks, key=lambda b: b.bbox.y)

        lines: List[TextLine] = []

        for block in sorted_by_y:
            placed = False
            for line in lines:
                if line.can_include(block):
                    line.add_block(block)
                    placed = True
                    break

            if not placed:
                new_line = TextLine(
                    y_reference=block.bbox.y,
                    tolerance=self.vertical_tolerance
                )
                new_line.add_block(block)
                lines.append(new_line)

        # Sort the assembled lines vertically from top to bottom
        lines.sort(key=lambda l: l.y_reference)

        return [l.get_sorted_text() for l in lines]