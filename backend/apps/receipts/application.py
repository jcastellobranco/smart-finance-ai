"""Receipt application orchestration, independent from HTTP views."""
from django.db import transaction

from .tasks import process_receipt_task


def create_receipt(*, serializer, user):
    with transaction.atomic():
        receipt = serializer.save(uploaded_by=user)
        transaction.on_commit(
            lambda receipt_id=receipt.pk: process_receipt_task.delay(receipt_id)
        )
    return receipt
