from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.expenses.models import ExpenseCategory
from .application import create_receipt
from .review import confirm_receipt
from .selectors import visible_receipts
from .serializers import ReceiptUploadSerializer


class ReceiptConfirmationSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    merchant = serializers.CharField(max_length=120, required=False, allow_blank=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    expense_date = serializers.DateField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(), required=False, allow_null=True
    )


class ReceiptUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return visible_receipts(self.request.user)

    def perform_create(self, serializer):
        create_receipt(serializer=serializer, user=self.request.user)

    @action(detail=True, methods=["post"], parser_classes=[FormParser, MultiPartParser])
    def confirm(self, request, pk=None):
        receipt = self.get_object()
        serializer = ReceiptConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expense = confirm_receipt(
            receipt_id=receipt.pk, user=request.user,
            validated_data=serializer.validated_data,
        )
        return Response({"expense_id": expense.pk, "status": "completed"})
