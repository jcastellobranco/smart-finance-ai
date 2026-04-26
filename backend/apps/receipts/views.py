from rest_framework import viewsets

from .models import ReceiptUpload
from .serializers import ReceiptUploadSerializer
from .tasks import process_receipt_task


class ReceiptUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptUploadSerializer

    def get_queryset(self):
        return ReceiptUpload.objects.filter(
            household__members__user=self.request.user
        ).select_related("household", "uploaded_by").distinct()

    def perform_create(self, serializer):
        receipt = serializer.save(uploaded_by=self.request.user)
        process_receipt_task.delay(receipt.id)