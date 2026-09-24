import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image, ImageDraw, ImageFont

from visitext.engine import VisiTextEngine
from visitext.models import BoundingBox, TextBlock
from visitext.table_exporter import TableExporter
from visitext.visualizer import Visualizer


class TestVisiTextEndToEnd(unittest.TestCase):
    """End-to-End pipeline verification: image generation, processing, and multi-format exports."""

    @staticmethod
    def _create_mock_invoice_image(output_path: Path) -> None:
        width, height = 800, 600
        img = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        draw.rectangle([(20, 20), (780, 580)], outline=(180, 180, 180), width=2)
        draw.text((40, 40), "VISITEXT TECHNOLOGIES INC.", fill=(0, 0, 0), font=font)
        draw.text((40, 110), "Invoice: INV-2026-09", fill=(0, 0, 0), font=font)
        draw.text((40, 130), "Date: 2026-09-21", fill=(0, 0, 0), font=font)
        draw.text((40, 330), "Total: $1000.00", fill=(0, 0, 0), font=font)

        img.save(str(output_path))

    def test_full_pipeline_mock_ocr_and_export(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            sample_img_path = temp_path / "mock_invoice.png"
            output_dir = temp_path / "outputs"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Step 1: Generate real synthetic invoice image via internal helper
            self._create_mock_invoice_image(sample_img_path)
            self.assertTrue(sample_img_path.exists(), "Sample invoice image must be generated on disk.")

            # Step 2: Initialize Core Engine & Modules
            engine = VisiTextEngine(confidence_threshold=40.0)
            visualizer = Visualizer()
            table_exporter = TableExporter()

            # Mock pytesseract payload to make test fully portable across environments
            mock_ocr_payload = {
                "text": ["", "Invoice:", "INV-2026-09", "Total:", "$1000.00", ""],
                "conf": ["-1", "95.0", "92.0", "88.0", "96.0", "-1"],
                "left": [0, 40, 120, 40, 120, 0],
                "top": [0, 110, 110, 330, 330, 0],
                "width": [0, 60, 100, 50, 80, 0],
                "height": [0, 20, 20, 20, 20, 0],
                "block_num": [0, 1, 1, 2, 2, 0],
                "line_num": [0, 1, 1, 1, 1, 0]
            }

            with patch("pytesseract.image_to_data", return_value=mock_ocr_payload):
                document = engine.process(
                    image_input=sample_img_path,
                    apply_preprocessing=True,
                    use_clahe=True,
                    clahe_clip_limit=2.0
                )

            # Step 3: Validate structured document results
            self.assertIn("Invoice: INV-2026-09", document.clean_text)
            self.assertEqual(len(document.lines), 2)
            self.assertEqual(document.lines[0], "Invoice: INV-2026-09")
            self.assertEqual(document.lines[1], "Total: $1000.00")
            self.assertEqual(document.entities.get("key_value_pairs", {}).get("Invoice"), "INV-2026-09")

            # Step 4: Export to all supported formats
            base_name = sample_img_path.stem

            txt_file = output_dir / f"{base_name}.txt"
            txt_file.write_text(document.clean_text, encoding="utf-8")

            json_file = output_dir / f"{base_name}.json"
            json_file.write_text(document.model_dump_json(indent=2), encoding="utf-8")

            rows = table_exporter.parse_lines_to_rows(document.lines)
            csv_file = output_dir / f"{base_name}.csv"
            csv_file.write_text(table_exporter.to_csv(rows), encoding="utf-8")

            md_file = output_dir / f"{base_name}.md"
            md_file.write_text(table_exporter.to_markdown(rows), encoding="utf-8")

            annotated_file = output_dir / f"{base_name}_annotated.png"
            visualizer.draw_bboxes(
                image_input=sample_img_path,
                blocks=document.blocks,
                output_path=annotated_file
            )

            # Step 5: Verify existence and integrity of every generated artifact
            self.assertTrue(txt_file.exists(), "TXT output must exist.")
            self.assertTrue(json_file.exists(), "JSON output must exist.")
            self.assertTrue(csv_file.exists(), "CSV output must exist.")
            self.assertTrue(md_file.exists(), "Markdown output must exist.")
            self.assertTrue(annotated_file.exists(), "Annotated PNG output must exist.")

            # Validate JSON content integrity
            parsed_json = json.loads(json_file.read_text(encoding="utf-8"))
            self.assertIn("metadata", parsed_json)
            self.assertEqual(parsed_json["metadata"]["clahe_enabled"], True)
            self.assertEqual(len(parsed_json["blocks"]), 4)

            # Validate CSV content
            csv_data = csv_file.read_text(encoding="utf-8")
            self.assertIn("Invoice: INV-2026-09", csv_data)

            # Validate Markdown formatting
            md_data = md_file.read_text(encoding="utf-8")
            self.assertIn("| ---", md_data)


if __name__ == "__main__":
    unittest.main()