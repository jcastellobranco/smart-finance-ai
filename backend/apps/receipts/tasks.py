import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from apps.expenses.models import Expense, ExpenseCategory
from .models import ReceiptUpload
from .services import fake_extract_receipt_data, normalize_amount

logger = logging.getLogger(__name__)


@shared_task
def process_receipt_task(receipt_id: int):
    # A row lock serializes concurrent deliveries of the same task.
    with transaction.atomic():
        receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
        if receipt.status == ReceiptUpload.Status.COMPLETED:
            return
        # Do not create an expense twice even if a previous worker crashed
        # after inserting it but before marking the receipt completed.
        if Expense.objects.filter(receipt_upload_id=receipt_id).exists():
            receipt.status = ReceiptUpload.Status.COMPLETED
            receipt.processed_at = timezone.now()
            receipt.save(update_fields=["status", "processed_at"])
            return
        receipt.status = ReceiptUpload.Status.PROCESSING
        receipt.error_message = ""
        receipt.save(update_fields=["status", "error_message"])

    try:
        extracted = fake_extract_receipt_data(receipt.file.path)
        amount = normalize_amount(extracted.get("amount", "0"))
        if amount <= 0:
            raise ValueError("Extracted receipt amount must be positive.")

        with transaction.atomic():
            receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
            if receipt.status == ReceiptUpload.Status.COMPLETED:
                return
            category, _ = ExpenseCategory.objects.get_or_create(
                name=extracted.get("category", "Other")
            )
            Expense.objects.get_or_create(
                receipt_upload=receipt,
                defaults={
                    "household": receipt.household,
                    "paid_by": receipt.uploaded_by,
                    "category": category,
                    "description": extracted.get("description", "Receipt expense"),
                    "merchant": extracted.get("merchant", ""),
                    "amount": amount,
                    "expense_date": extracted.get("date"),
                    "source": Expense.Source.RECEIPT,
                },
            )
            receipt.raw_text = extracted.get("raw_text", "")
            receipt.extracted_data = extracted
            receipt.status = ReceiptUpload.Status.COMPLETED
            receipt.processed_at = timezone.now()
            receipt.error_message = ""
            receipt.save(update_fields=[
                "raw_text", "extracted_data", "status", "processed_at", "error_message"
            ])
    except Exception:
        logger.exception("Receipt processing failed for receipt_id=%s", receipt_id)
        with transaction.atomic():
            receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
            if receipt.status != ReceiptUpload.Status.COMPLETED:
                receipt.status = ReceiptUpload.Status.FAILED
                receipt.error_message = "Receipt processing failed."
                receipt.save(update_fields=["status", "error_message"])
        raise
