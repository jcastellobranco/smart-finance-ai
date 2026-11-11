"""Explicit user approval is required before posting receipt-derived expenses."""
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.expenses.models import Expense
from .models import ReceiptUpload
from .services import normalize_amount


@transaction.atomic
def confirm_receipt(*, receipt_id, user, validated_data):
    receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
    if receipt.status == ReceiptUpload.Status.COMPLETED:
        return Expense.objects.get(receipt_upload=receipt)
    if receipt.status != ReceiptUpload.Status.REVIEW:
        raise ValidationError({"status": "Receipt is not ready for review."})
    amount = normalize_amount(validated_data["amount"])
    expense, _ = Expense.objects.get_or_create(
        receipt_upload=receipt,
        defaults={
            "household": receipt.household,
            "paid_by": user,
            "category": validated_data.get("category"),
            "description": validated_data["description"],
            "merchant": validated_data.get("merchant", ""),
            "amount": amount,
            "expense_date": validated_data["expense_date"],
            "source": Expense.Source.RECEIPT,
        },
    )
    receipt.status = ReceiptUpload.Status.COMPLETED
    receipt.save(update_fields=["status"])
    return expense
