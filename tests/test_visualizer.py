import unittest
import numpy as np
from visitext.models import TextBlock, BoundingBox
from visitext.visualizer import Visualizer


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = Visualizer()

    def test_confidence_colors(self):
        green = self.visualizer.get_color_by_confidence(85.0)
        orange = self.visualizer.get_color_by_confidence(60.0)
        red = self.visualizer.get_color_by_confidence(30.0)

        self.assertEqual(green, (0, 200, 0))
        self.assertEqual(orange, (0, 165, 255))
        self.assertEqual(red, (0, 0, 255))

    def test_draw_bboxes_on_blank_matrix(self):
        # Create a black blank canvas (100x100 RGB)
        blank = np.zeros((100, 100, 3), dtype=np.uint8)
        block = TextBlock(
            text="Test",
            confidence=90.0,
            bbox=BoundingBox(x=10, y=10, width=40, height=20)
        )

        result = self.visualizer.draw_bboxes(blank, [block], draw_labels=False)
        self.assertEqual(result.shape, (100, 100, 3))
        # Verify drawing occurred (array is not completely zeros anymore)
        self.assertTrue(np.any(result > 0))


if __name__ == "__main__":
    unittest.main()