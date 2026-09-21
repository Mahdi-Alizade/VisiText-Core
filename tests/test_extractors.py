import unittest
from visitext.extractors import DocumentDataExtractor


class TestDocumentDataExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = DocumentDataExtractor()

    def test_extract_invoice_and_dates(self):
        text = "Tax Invoice: INV-98234 Date: 2026-09-21 Contact: billing@visitext.io"
        lines = [
            "Invoice: INV-98234",
            "Date: 2026-09-21",
            "Total Amount: $1,450.00"
        ]

        data = self.extractor.extract(lines=lines, full_text=text)

        self.assertIn("INV-98234", data.invoice_numbers)
        self.assertIn("2026-09-21", data.dates)
        self.assertIn("billing@visitext.io", data.emails)
        self.assertEqual(data.key_value_pairs.get("Invoice"), "INV-98234")
        self.assertEqual(data.key_value_pairs.get("Date"), "2026-09-21")
        self.assertEqual(data.key_value_pairs.get("Total Amount"), "$1,450.00")


if __name__ == "__main__":
    unittest.main()