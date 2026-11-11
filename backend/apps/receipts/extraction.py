"""OCR provider boundary. No external LLM calls or fabricated receipt values."""
from dataclasses import dataclass
from pathlib import Path
import re

from django.conf import settings


@dataclass(frozen=True)
class ExtractionResult:
    raw_text: str
    fields: dict


class ExtractionError(Exception):
    pass


def extract_receipt(file_path: str) -> ExtractionResult:
    path = Path(file_path)
    extension = path.suffix.lower()
    if extension == ".pdf":
        import pymupdf
        with pymupdf.open(path) as doc:
            if len(doc) > 10:
                raise ExtractionError("PDF exceeds the ten-page processing limit.")
            text = "\n".join(page.get_text() for page in doc)
            if not text.strip():
                raise ExtractionError("Scanned PDF needs a dedicated OCR provider.")
    elif extension in {".png", ".jpg", ".jpeg", ".webp"}:
        import pytesseract
        from PIL import Image
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            text = pytesseract.image_to_string(
                image, lang=getattr(settings, "RECEIPT_OCR_LANGUAGE", "por")
            )
    else:
        raise ExtractionError("Unsupported receipt format.")

    if not text.strip():
        raise ExtractionError("No text was detected.")

    # Conservative heuristics: never invent a merchant, date, or total.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    total_match = re.search(
        r"(?im)^\s*(?:total(?:\s+a\s+pagar)?|valor\s+total)\s*[:R$\s]*([\d.,]+)\s*$",
        text,
    )
    fields = {
        "merchant": lines[0][:120] if lines else "",
        "description": "",
        "amount": total_match.group(1) if total_match else None,
        "date": None,
        "category": None,
    }
    return ExtractionResult(raw_text=text[:20000], fields=fields)
