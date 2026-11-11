"""Normalization and compatibility utilities for receipt extraction."""
from decimal import Decimal, InvalidOperation


def normalize_amount(value: str) -> Decimal:
    if value is None:
        raise ValueError("Missing amount")
    cleaned = str(value).strip().replace("R$", "").replace(" ", "")
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        amount = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError("Invalid amount") from exc
    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be positive and finite")
    return amount.quantize(Decimal("0.01"))
