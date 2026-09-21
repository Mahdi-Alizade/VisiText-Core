import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ExtractedDocumentData(BaseModel):
    invoice_numbers: List[str] = Field(default_factory=list)
    dates: List[str] = Field(default_factory=list)
    monetary_amounts: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    key_value_pairs: Dict[str, str] = Field(default_factory=dict)


class DocumentDataExtractor:
    """Extracts business-critical entities and structured key-value pairs from text lines."""

    # Standard Regex Patterns
    INVOICE_PATTERN = r'(?i)\b(?:inv(?:oice)?|bill|receipt)[\s#.:-]*([a-z0-9-]+)\b'
    DATE_PATTERN = r'\b(?:\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})\b'
    MONEY_PATTERN = r'(?:[\$€£]|USD|EUR|GBP)?\s?\b\d{1,3}(?:[,\s]\d{3})*(?:\.\d{1,2})?\s?(?:[\$€£]|USD|EUR|GBP)?\b'
    EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    KEY_VALUE_PATTERN = r'^\s*([A-Za-z0-9\s]{2,25})\s*[:=]\s*(.+)$'

    def extract(self, lines: List[str], full_text: str) -> ExtractedDocumentData:
        extracted = ExtractedDocumentData()

        # Extract scalar global entities
        extracted.invoice_numbers = list(set(re.findall(self.INVOICE_PATTERN, full_text)))
        extracted.dates = list(set(re.findall(self.DATE_PATTERN, full_text)))
        extracted.emails = list(set(re.findall(self.EMAIL_PATTERN, full_text)))

        # Extract monetary candidates
        potential_amounts = re.findall(self.MONEY_PATTERN, full_text)
        cleaned_amounts = [
            amt.strip() for amt in potential_amounts
            if any(char.isdigit() for char in amt) and len(amt.strip()) > 1
        ]
        extracted.monetary_amounts = list(set(cleaned_amounts))

        # Extract key-value pairs from reconstructed layout lines
        kv_dict: Dict[str, str] = {}
        for line in lines:
            match = re.match(self.KEY_VALUE_PATTERN, line)
            if match:
                key = match.group(1).strip()
                val = match.group(2).strip()
                kv_dict[key] = val

        extracted.key_value_pairs = kv_dict
        return extracted