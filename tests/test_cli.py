import unittest
from pathlib import Path
from unittest.mock import patch
from visitext.cli import collect_image_files


class TestCliHelpers(unittest.TestCase):
    def test_collect_image_files_filters_extensions(self):
        with patch.object(Path, "is_file", return_value=True):
            png_file = Path("dummy.png")
            txt_file = Path("dummy.txt")

            self.assertEqual(collect_image_files(png_file), [png_file])
            self.assertEqual(collect_image_files(txt_file), [])


if __name__ == "__main__":
    unittest.main()