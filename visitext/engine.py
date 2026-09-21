import os
import time
from typing import Union, List, Optional
from pathlib import Path
import numpy as np
import pytesseract
from pytesseract import Output
from dotenv import load_dotenv

from visitext.models import ProcessedDocument, TextBlock, BoundingBox
from visitext.preprocessor import ImagePreprocessor
from visitext.filters import TextFilter
from visitext.layout import LayoutReconstructor

load_dotenv()


class VisiTextEngine:
    """Core OCR processing engine managing the pipeline from image to structured data."""

    def __init__(
        self,
        tesseract_cmd: Optional[str] = None,
        default_lang: str = "eng",
        confidence_threshold: float = 40.0
    ):
        cmd = tesseract_cmd or os.getenv("TESSERACT_CMD")
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd

        self.default_lang = default_lang
        self.confidence_threshold = confidence_threshold
        self.preprocessor = ImagePreprocessor()
        self.filter = TextFilter()
        self.layout_reconstructor = LayoutReconstructor(vertical_tolerance=12)

    def process(
        self,
        image_input: Union[str, Path, np.ndarray],
        lang: Optional[str] = None,
        apply_preprocessing: bool = True
    ) -> ProcessedDocument:
        start_time = time.time()
        selected_lang = lang or self.default_lang

        if apply_preprocessing:
            processed_img = self.preprocessor.process(image_input)
        else:
            processed_img = self.preprocessor.load_image(image_input)

        ocr_data = pytesseract.image_to_data(
            processed_img,
            lang=selected_lang,
            output_type=Output.DICT
        )

        blocks: List[TextBlock] = []
        raw_words: List[str] = []

        total_entries = len(ocr_data["text"])
        for i in range(total_entries):
            word = ocr_data["text"][i].strip()
            conf_str = ocr_data["conf"][i]

            try:
                conf = float(conf_str)
            except (ValueError, TypeError):
                conf = -1.0

            if word and conf >= self.confidence_threshold:
                bbox = BoundingBox(
                    x=int(ocr_data["left"][i]),
                    y=int(ocr_data["top"][i]),
                    width=int(ocr_data["width"][i]),
                    height=int(ocr_data["height"][i])
                )
                block = TextBlock(
                    text=word,
                    confidence=conf,
                    bbox=bbox,
                    block_num=int(ocr_data["block_num"][i]),
                    line_num=int(ocr_data["line_num"][i])
                )
                blocks.append(block)
                raw_words.append(word)

        raw_text = " ".join(raw_words)
        clean_text = self.filter.clean(raw_text)
        reconstructed_lines = self.layout_reconstructor.reconstruct_lines(blocks)
        execution_time = round(time.time() - start_time, 4)

        return ProcessedDocument(
            raw_text=raw_text,
            clean_text=clean_text,
            lines=reconstructed_lines,
            blocks=blocks,
            metadata={
                "language": selected_lang,
                "confidence_threshold": self.confidence_threshold,
                "preprocessing_applied": apply_preprocessing,
                "execution_seconds": execution_time,
                "total_blocks_found": len(blocks),
                "total_lines_reconstructed": len(reconstructed_lines)
            }
        )