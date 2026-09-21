import unittest
from visitext.models import TextBlock, BoundingBox
from visitext.layout import LayoutReconstructor


class TestLayoutReconstructor(unittest.TestCase):
    def setUp(self):
        self.reconstructor = LayoutReconstructor(vertical_tolerance=10)

    def test_reconstruct_lines_groups_and_sorts_correctly(self):
        # Construct synthetic OCR tokens out of order
        token_a = TextBlock(
            text="Invoice",
            confidence=95.0,
            bbox=BoundingBox(x=10, y=100, width=50, height=20)
        )
        token_b = TextBlock(
            text="Total:",
            confidence=90.0,
            bbox=BoundingBox(x=10, y=200, width=40, height=20)
        )
        token_c = TextBlock(
            text="Number:",
            confidence=94.0,
            bbox=BoundingBox(x=70, y=102, width=60, height=20)
        )
        token_d = TextBlock(
            text="$500.00",
            confidence=98.0,
            bbox=BoundingBox(x=60, y=198, width=50, height=20)
        )

        blocks = [token_d, token_a, token_b, token_c]
        lines = self.reconstructor.reconstruct_lines(blocks)

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], "Invoice Number:")
        self.assertEqual(lines[1], "Total: $500.00")

    def test_reconstruct_lines_handles_empty_blocks(self):
        lines = self.reconstructor.reconstruct_lines([])
        self.assertEqual(lines, [])


if __name__ == "__main__":
    unittest.main()