"""Background OCR; extraction never creates an unreviewed expense."""
import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .extraction import extract_receipt
from .models import ReceiptUpload

logger = logging.getLogger(__name__)


@shared_task
def process_receipt_task(receipt_id: int):
    with transaction.atomic():
        receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
        if receipt.status in {ReceiptUpload.Status.COMPLETED, ReceiptUpload.Status.REVIEW}:
            return
        receipt.status = ReceiptUpload.Status.PROCESSING
        receipt.error_message = ""
        receipt.save(update_fields=["status", "error_message"])

    try:
        receipt = ReceiptUpload.objects.get(pk=receipt_id)
        result = extract_receipt(receipt.file.path)
        with transaction.atomic():
            receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
            if receipt.status in {ReceiptUpload.Status.COMPLETED, ReceiptUpload.Status.REVIEW}:
                return
            receipt.raw_text = result.raw_text
            receipt.extracted_data = result.fields
            receipt.status = ReceiptUpload.Status.REVIEW
            receipt.processed_at = timezone.now()
            receipt.save(update_fields=[
                "raw_text", "extracted_data", "status", "processed_at"
            ])
    except Exception:
        logger.exception("Receipt extraction failed for receipt_id=%s", receipt_id)
        with transaction.atomic():
            receipt = ReceiptUpload.objects.select_for_update().get(pk=receipt_id)
            if receipt.status not in {ReceiptUpload.Status.COMPLETED, ReceiptUpload.Status.REVIEW}:
                receipt.status = ReceiptUpload.Status.FAILED
                receipt.error_message = "Receipt extraction failed; try a clearer image."
                receipt.save(update_fields=["status", "error_message"])
        raise
