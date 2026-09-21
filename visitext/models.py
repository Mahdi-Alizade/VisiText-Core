from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: int = Field(..., description="Top-left X coordinate")
    y: int = Field(..., description="Top-left Y coordinate")
    width: int = Field(..., description="Width of the detected bounding box")
    height: int = Field(..., description="Height of the detected bounding box")


class TextBlock(BaseModel):
    text: str = Field(..., description="Recognized text fragment")
    confidence: float = Field(..., description="Confidence score from 0.0 to 100.0")
    bbox: Optional[BoundingBox] = Field(None, description="Spatial coordinates of the text")
    block_num: Optional[int] = Field(None, description="Paragraph or segment block identifier")
    line_num: Optional[int] = Field(None, description="Line identifier inside block")


class ProcessedDocument(BaseModel):
    raw_text: str = Field(..., description="Full unprocessed aggregated text")
    clean_text: str = Field(..., description="Normalized and filtered text")
    lines: List[str] = Field(default_factory=list, description="Spatially reconstructed reading lines")
    blocks: List[TextBlock] = Field(default_factory=list, description="Extracted blocks with coordinates")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata including engine, params, execution time")