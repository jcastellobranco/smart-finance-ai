from django.db import transaction
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import ReceiptUpload
from .serializers import ReceiptUploadSerializer
from .tasks import process_receipt_task


class ReceiptUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return ReceiptUpload.objects.filter(
            household__members__user=self.request.user
        ).select_related("household", "uploaded_by").distinct()

    def perform_create(self, serializer):
        with transaction.atomic():
            receipt = serializer.save(uploaded_by=self.request.user)
            transaction.on_commit(lambda: process_receipt_task.delay(receipt.pk))
