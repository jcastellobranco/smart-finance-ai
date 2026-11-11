from django.conf import settings
from django.db import models

from apps.households.models import Household


class ReceiptUpload(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        REVIEW = "review", "Needs review"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="receipts",
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receipt_uploads",
    )

    file = models.FileField(upload_to="receipts/")
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )

    raw_text = models.TextField(blank=True)
    extracted_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Receipt {self.id} - {self.status}"