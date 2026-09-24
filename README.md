# VisiText-Core

A modular, production-ready Python OCR engine designed for structured text extraction, layout reconstruction, entity parsing, and visual bounding box diagnostics from scanned and photographed document images.

---

## Key Features

- **Adaptive Image Preprocessing**: Deskew correction, median blur denoising, and **CLAHE** (Contrast Limited Adaptive Histogram Equalization) for dark or unevenly exposed scans.
- **Spatial Layout Reconstruction**: Clusters flat token streams into ordered reading lines preserving column arrangements and table spacing.
- **Entity & Key-Value Extraction**: Automatic regex parsing for invoice identifiers, dates, email addresses, monetary values, and arbitrary `Key: Value` pairs.
- **Multi-Format Tabular Exports**: Directly export extracted document structures into **JSON**, **TXT**, **CSV**, and formatted **Markdown** tables.
- **Visual Diagnostics**: Renders confidence-coded bounding boxes directly onto document copies (Green: $\ge 80\%$, Orange: $\ge 50\%$, Red: $< 50\%$).
- **Fully Tested & Modular**: Comprehensive Pytest suite covering preprocessors, spatial algorithms, exporters, CLI helpers, and end-to-end integration workflows.

---

## Directory Architecture

VisiText-Core/├── .gitignore├── .env.example├── requirements.txt├── pytest.ini├── README.md├── generate_sample.py├── visitext/│   ├── init.py│   ├── models.py            # Pydantic schemas (ProcessedDocument, TextBlock, BoundingBox)│   ├── preprocessor.py      # OpenCV CLAHE, deskew, and adaptive threshold pipeline│   ├── filters.py           # Whitespace normalization and OCR artifact sanitization│   ├── layout.py            # Spatial clustering and reading-order line reconstruction│   ├── extractors.py        # Business entity and key-value pattern extraction│   ├── table_exporter.py    # Structured row parsing to CSV and Markdown tables│   ├── visualizer.py        # OpenCV bounding box overlay with confidence badges│   ├── engine.py            # Unified OCR execution orchestrator│   └── cli.py               # Robust command-line interface└── tests/├── test_cli.py├── test_extractors.py├── test_filters.py├── test_layout.py├── test_preprocessor.py├── test_table_exporter.py├── test_visualizer.py└── test_e2e.py
---

## Setup & Installation

### 1. Environment Setup

Ensure you are inside the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
2. Tesseract-OCR Engine SetupInstall Tesseract-OCR on Windows. If installed outside standard PATH, set the path in .env:Code snippetTESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
CLI UsageThe CLI handles single files or entire directories containing supported image formats (.png, .jpg, .jpeg, .bmp, .tiff, .webp).Basic Extraction (All Formats)PowerShellpython -m visitext.cli document.png -f all -o outputs
Advanced Extraction with CLAHE & Visual OverlaysPowerShellpython -m visitext.cli input_scan.png -v --clahe-clip-limit 3.0 --confidence 45.0 -f all -o outputs
Available CLI FlagsFlagTypeDefaultDescriptioninput_pathPositionalRequiredPath to single image or directory of images.-o, --output-dirStringoutputsTarget directory for generated output files.-f, --formatChoiceallOutput format: json, txt, csv, md, all.-l, --langStringengTesseract language code (e.g., eng, fas, eng+fas).-c, --confidenceFloat40.0Minimum confidence score threshold (0.0 to 100.0).--no-preprocessFlagFalseDisables deskew and adaptive threshold binarization.--no-claheFlagFalseDisables adaptive CLAHE contrast enhancement.--clahe-clip-limitFloat2.0Contrast clipping limit for the CLAHE algorithm.-v, --visualizeFlagFalseGenerates {stem}_annotated.png with color-coded bounding boxes.Python API ExamplePythonfrom visitext import VisiTextEngine

engine = VisiTextEngine(default_lang="eng", confidence_threshold=50.0)

# Process image through end-to-end pipeline
document = engine.process(
    image_input="sample_invoice.png",
    apply_preprocessing=True,
    use_clahe=True,
    clahe_clip_limit=2.5
)

# Access clean text
print(document.clean_text)

# Access spatially reconstructed lines
for line in document.lines:
    print(line)

# Access parsed entities
print("Invoices:", document.entities["invoice_numbers"])
print("Dates:", document.entities["dates"])
print("Key-Values:", document.entities["key_value_pairs"])
Running the Test SuiteExecute all unit and end-to-end integration tests using pytest:PowerShellpython -m pytest tes