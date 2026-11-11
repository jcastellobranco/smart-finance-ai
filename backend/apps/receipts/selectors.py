"""Read-side queries for the receipts domain."""
from .models import ReceiptUpload


def visible_receipts(user):
    return (
        ReceiptUpload.objects.filter(household__members__user=user)
        .select_related("household", "uploaded_by")
        .distinct()
    )
