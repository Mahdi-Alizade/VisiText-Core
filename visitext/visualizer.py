from pathlib import Path
from typing import Union, Tuple, List, Optional
import cv2
import numpy as np

from visitext.models import TextBlock
from visitext.preprocessor import ImagePreprocessor


class Visualizer:
    """Draws detected bounding boxes, recognized text, and confidence scores onto images."""

    @staticmethod
    def get_color_by_confidence(confidence: float) -> Tuple[int, int, int]:
        # Green for high confidence (>= 80), Orange for medium (>= 50), Red for low (< 50)
        # OpenCV uses BGR ordering
        if confidence >= 80.0:
            return (0, 200, 0)
        elif confidence >= 50.0:
            return (0, 165, 255)
        else:
            return (0, 0, 255)

    def draw_bboxes(
        self,
        image_input: Union[str, Path, np.ndarray],
        blocks: List[TextBlock],
        output_path: Optional[Union[str, Path]] = None,
        draw_labels: bool = True
    ) -> np.ndarray:
        image = ImagePreprocessor.load_image(image_input)
        annotated = image.copy()

        for block in blocks:
            if not block.bbox:
                continue

            x = block.bbox.x
            y = block.bbox.y
            w = block.bbox.width
            h = block.bbox.height
            conf = block.confidence

            color = self.get_color_by_confidence(conf)

            # Draw outer rectangle
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)

            if draw_labels:
                label = f"{block.text} ({int(conf)}%)"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.4
                thickness = 1

                (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                label_y = max(y - 5, text_h + 5)

                # Draw label background badge
                cv2.rectangle(
                    annotated,
                    (x, label_y - text_h - 2),
                    (x + text_w + 2, label_y + 2),
                    color,
                    -1
                )

                # Draw white text label inside badge
                cv2.putText(
                    annotated,
                    label,
                    (x + 1, label_y),
                    font,
                    font_scale,
                    (255, 255, 255),
                    thickness,
                    lineType=cv2.LINE_AA
                )

        if output_path:
            out_file = Path(output_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(out_file), annotated)

        return annotated