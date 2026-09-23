import argparse
import json
import sys
from pathlib import Path
from typing import List

from visitext.engine import VisiTextEngine
from visitext.visualizer import Visualizer


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}


def collect_image_files(target_path: Path) -> List[Path]:
    if target_path.is_file():
        if target_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [target_path]
        return []
    elif target_path.is_dir():
        return [
            file
            for file in target_path.iterdir()
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    return []


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        prog="visitext",
        description="VisiText-Core: Structured OCR and text processing engine for document images."
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to an image file or directory containing image files."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="outputs",
        help="Directory where extraction results will be stored (default: outputs)."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "txt", "both"],
        default="both",
        help="Output format to save (default: both)."
    )
    parser.add_argument(
        "-l", "--lang",
        type=str,
        default="eng",
        help="Tesseract language code(s) (e.g. eng, fas, eng+fas)."
    )
    parser.add_argument(
        "-c", "--confidence",
        type=float,
        default=40.0,
        help="Confidence threshold score from 0 to 100 (default: 40.0)."
    )
    parser.add_argument(
        "--no-preprocess",
        action="store_true",
        help="Disable OpenCV deskew and adaptive threshold binarization."
    )
    parser.add_argument(
        "--no-clahe",
        action="store_true",
        help="Disable CLAHE adaptive contrast equalization during preprocessing."
    )
    parser.add_argument(
        "--clahe-clip-limit",
        type=float,
        default=2.0,
        help="Threshold for contrast limiting in CLAHE algorithm (default: 2.0)."
    )
    parser.add_argument(
        "-v", "--visualize",
        action="store_true",
        help="Generate and save an annotated image highlighting detected bounding boxes."
    )

    args = parser.parse_args()

    target_path = Path(args.input_path)
    if not target_path.exists():
        print(f"Error: Target path '{args.input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    images = collect_image_files(target_path)
    if not images:
        print(f"Error: No valid image files found in '{args.input_path}'.", file=sys.stderr)
        sys.exit(1)

    output_directory = Path(args.output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    engine = VisiTextEngine(
        default_lang=args.lang,
        confidence_threshold=args.confidence
    )
    visualizer = Visualizer()

    print(f"Starting extraction for {len(images)} image(s)...")

    for index, img_path in enumerate(images, start=1):
        print(f"[{index}/{len(images)}] Processing: {img_path.name}")
        try:
            document = engine.process(
                image_input=img_path,
                lang=args.lang,
                apply_preprocessing=not args.no_preprocess,
                use_clahe=not args.no_clahe,
                clahe_clip_limit=args.clahe_clip_limit
            )

            base_name = img_path.stem

            if args.format in ["txt", "both"]:
                txt_path = output_directory / f"{base_name}.txt"
                txt_path.write_text(document.clean_text, encoding="utf-8")
                print(f"  -> Saved text: {txt_path}")

            if args.format in ["json", "both"]:
                json_path = output_directory / f"{base_name}.json"
                json_path.write_text(
                    document.model_dump_json(indent=2),
                    encoding="utf-8"
                )
                print(f"  -> Saved metadata: {json_path}")

            if args.visualize:
                annotated_path = output_directory / f"{base_name}_annotated.png"
                visualizer.draw_bboxes(
                    image_input=img_path,
                    blocks=document.blocks,
                    output_path=annotated_path
                )
                print(f"  -> Saved visual overlay: {annotated_path}")

        except Exception as error:
            print(f"  -> Failed to process {img_path.name}: {error}", file=sys.stderr)

    print("Execution complete.")


if __name__ == "__main__":
    run_cli()