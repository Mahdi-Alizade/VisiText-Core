from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_sample_invoice(output_path: str = "sample_invoice.png") -> None:
    # Standard document canvas (800x600)
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Use default bitmap font
    font = ImageFont.load_default()

    # Draw border
    draw.rectangle([(20, 20), (780, 580)], outline=(180, 180, 180), width=2)

    # Document Header
    draw.text((40, 40), "VISITEXT TECHNOLOGIES INC.", fill=(0, 0, 0), font=font)
    draw.text((40, 60), "Official Processing & Billing Statement", fill=(100, 100, 100), font=font)

    # Key Value pairs
    draw.text((40, 110), "Invoice: INV-2026-09", fill=(0, 0, 0), font=font)
    draw.text((40, 130), "Date: 2026-09-21", fill=(0, 0, 0), font=font)
    draw.text((40, 150), "Email: contact@visitext.local", fill=(0, 0, 0), font=font)

    # Line separator
    draw.line([(40, 180), (760, 180)], fill=(200, 200, 200), width=1)

    # Table Headers
    draw.text((40, 200), "Description", fill=(0, 0, 0), font=font)
    draw.text((400, 200), "Qty", fill=(0, 0, 0), font=font)
    draw.text((600, 200), "Price", fill=(0, 0, 0), font=font)

    # Table Rows
    draw.text((40, 230), "Document Preprocessing Pipeline", fill=(40, 40, 40), font=font)
    draw.text((400, 230), "1", fill=(40, 40, 40), font=font)
    draw.text((600, 230), "$350.00", fill=(40, 40, 40), font=font)

    draw.text((40, 260), "Structured Layout Reconstruction", fill=(40, 40, 40), font=font)
    draw.text((400, 260), "1", fill=(40, 40, 40), font=font)
    draw.text((600, 260), "$650.00", fill=(40, 40, 40), font=font)

    # Total Footer
    draw.line([(40, 310), (760, 310)], fill=(200, 200, 200), width=1)
    draw.text((500, 330), "Total: $1000.00", fill=(0, 0, 0), font=font)

    img.save(output_path)
    print(f"Sample invoice generated successfully: {Path(output_path).resolve()}")


if __name__ == "__main__":
    create_sample_invoice()