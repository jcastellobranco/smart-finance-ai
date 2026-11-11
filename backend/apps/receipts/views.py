from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .application import create_receipt
from .selectors import visible_receipts
from .serializers import ReceiptUploadSerializer


class ReceiptUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return visible_receipts(self.request.user)

    def perform_create(self, serializer):
        create_receipt(serializer=serializer, user=self.request.user)
