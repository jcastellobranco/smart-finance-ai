from decimal import Decimal
from datetime import date


def fake_extract_receipt_data(file_path: str) -> dict:
    """
    MVP fake extractor.

    Depois você troca isso por:
    - OCR real
    - regex
    - LLM classification
    """

    return {
        "merchant": "Example Market",
        "description": "Receipt expense",
        "amount": "89.90",
        "date": str(date.today()),
        "category": "Groceries",
        "raw_text": "Example OCR text extracted from receipt.",
    }


def normalize_amount(value: str) -> Decimal:
    return Decimal(str(value).replace(",", "."))