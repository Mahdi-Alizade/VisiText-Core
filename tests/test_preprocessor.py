import unittest
import numpy as np
from visitext.preprocessor import ImagePreprocessor


class TestImagePreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = ImagePreprocessor()

    def test_apply_clahe_enhances_contrast(self):
        # Create a low-contrast synthetic gray image (values between 100 and 115)
        low_contrast = np.random.randint(100, 115, size=(64, 64), dtype=np.uint8)

        enhanced = self.preprocessor.apply_clahe(low_contrast, clip_limit=3.0)

        self.assertEqual(enhanced.shape, (64, 64))
        # CLAHE stretches histogram, so standard deviation must increase
        self.assertGreaterEqual(float(np.std(enhanced)), float(np.std(low_contrast)))

    def test_process_runs_with_clahe(self):
        sample = np.ones((50, 50, 3), dtype=np.uint8) * 128
        result = self.preprocessor.process(sample, clahe_enabled=True, deskew_enabled=False)

        self.assertEqual(result.shape, (50, 50))
        # Result of adaptive threshold is binary (0 or 255)
        unique_values = np.unique(result)
        self.assertTrue(all(val in [0, 255] for val in unique_values))


if __name__ == "__main__":
    unittest.main()