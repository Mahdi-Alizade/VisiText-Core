import unittest
from visitext.filters import TextFilter


class TestTextFilter(unittest.TestCase):
    def setUp(self):
        self.filter = TextFilter()

    def test_normalize_whitespace(self):
        raw = "VisiText    Core \t\t Engine \n\n Test"
        expected = "VisiText Core Engine\nTest"
        result = self.filter.normalize_whitespace(raw)
        self.assertEqual(result, expected)

    def test_remove_isolated_symbols(self):
        raw = "Invoice Number # 1042 $ Total"
        cleaned = self.filter.remove_isolated_symbols(raw)
        self.assertNotIn("#", cleaned)
        self.assertNotIn("$", cleaned)

    def test_extract_patterns(self):
        sample = "Contact us at support@visitext.io or admin@visitext.io"
        emails = self.filter.extract_patterns(sample, r'[\w\.-]+@[\w\.-]+')
        self.assertEqual(len(emails), 2)
        self.assertIn("support@visitext.io", emails)


if __name__ == "__main__":
    unittest.main()