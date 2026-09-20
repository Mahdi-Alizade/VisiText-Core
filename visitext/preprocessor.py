import cv2
import numpy as np
from typing import Union, Tuple
from pathlib import Path


class ImagePreprocessor:
    """Handles image enhancement, noise reduction, and binarization for OCR."""

    @staticmethod
    def load_image(image_input: Union[str, Path, np.ndarray]) -> np.ndarray:
        if isinstance(image_input, (str, Path)):
            image_path = str(image_input)
            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError(f"Failed to load image from path: {image_path}")
            return img
        elif isinstance(image_input, np.ndarray):
            return image_input.copy()
        else:
            raise TypeError("Unsupported image input type. Provide a file path or numpy array.")

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def remove_noise(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        return cv2.medianBlur(image, kernel_size)

    @staticmethod
    def apply_adaptive_threshold(image: np.ndarray) -> np.ndarray:
        gray = ImagePreprocessor.to_grayscale(image)
        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

    @staticmethod
    def deskew(image: np.ndarray) -> np.ndarray:
        gray = ImagePreprocessor.to_grayscale(image)
        coords = np.column_stack(np.where(gray > 0))
        if coords.size == 0:
            return image
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            rotation_matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    def process(
        self,
        image_input: Union[str, Path, np.ndarray],
        deskew_enabled: bool = True,
        denoise_enabled: bool = True
    ) -> np.ndarray:
        image = self.load_image(image_input)
        if deskew_enabled:
            image = self.deskew(image)
        gray = self.to_grayscale(image)
        if denoise_enabled:
            gray = self.remove_noise(gray)
        processed = self.apply_adaptive_threshold(gray)
        return processed