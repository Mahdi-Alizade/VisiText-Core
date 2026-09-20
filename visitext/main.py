import json
from visitext import VisiTextEngine


def run_pipeline():
    engine = VisiTextEngine(default_lang="eng", confidence_threshold=50.0)

    # Example invocation using an image path
    image_file = "sample.png"
    print(f"Running VisiText-Core pipeline on target: {image_file}")

    try:
        result = engine.process(image_file, apply_preprocessing=True)
        print("\n=== Clean Extracted Text ===")
        print(result.clean_text)
        print("\n=== Structured JSON Metadata ===")
        print(json.dumps(result.metadata, indent=2))
    except FileNotFoundError:
        print(f"Please place a valid test image named '{image_file}' in the project root to run extraction.")


if __name__ == "__main__":
    run_pipeline()