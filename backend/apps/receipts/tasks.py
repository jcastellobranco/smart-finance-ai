from celery import shared_task
from django.utils import timezone

from apps.expenses.models import Expense, ExpenseCategory
from .models import ReceiptUpload
from .services import fake_extract_receipt_data, normalize_amount


@shared_task
def process_receipt_task(receipt_id: int):
    receipt = ReceiptUpload.objects.get(id=receipt_id)

    try:
        receipt.status = ReceiptUpload.Status.PROCESSING
        receipt.save(update_fields=["status"])

        extracted = fake_extract_receipt_data(receipt.file.path)

        category, _ = ExpenseCategory.objects.get_or_create(
            name=extracted.get("category", "Other")
        )

        Expense.objects.create(
            household=receipt.household,
            paid_by=receipt.uploaded_by,
            category=category,
            description=extracted.get("description", "Receipt expense"),
            merchant=extracted.get("merchant", ""),
            amount=normalize_amount(extracted.get("amount", "0")),
            expense_date=extracted.get("date"),
            source=Expense.Source.RECEIPT,
        )

        receipt.raw_text = extracted.get("raw_text", "")
        receipt.extracted_data = extracted
        receipt.status = ReceiptUpload.Status.COMPLETED
        receipt.processed_at = timezone.now()
        receipt.save(
            update_fields=[
                "raw_text",
                "extracted_data",
                "status",
                "processed_at",
            ]
        )

    except Exception as exc:
        receipt.status = ReceiptUpload.Status.FAILED
        receipt.error_message = str(exc)
        receipt.save(update_fields=["status", "error_message"])
        raise