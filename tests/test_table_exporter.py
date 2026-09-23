import unittest
from visitext.table_exporter import TableExporter


class TestTableExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = TableExporter()

    def test_parse_lines_and_csv_generation(self):
        lines = [
            "Item    Qty    Price",
            "Book    2      $40.00",
            "Pen     10     $15.00"
        ]
        rows = self.exporter.parse_lines_to_rows(lines)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ["Item", "Qty", "Price"])

        csv_text = self.exporter.to_csv(rows)
        self.assertIn("Item,Qty,Price", csv_text)
        self.assertIn("Book,2,$40.00", csv_text)

    def test_markdown_table_generation(self):
        rows = [
            ["Description", "Amount"],
            ["Hosting Service", "$120.00"]
        ]
        md_text = self.exporter.to_markdown(rows)
        self.assertIn("| Description", md_text)
        self.assertIn("| ---", md_text)
        self.assertIn("| Hosting Service", md_text)


if __name__ == "__main__":
    unittest.main()