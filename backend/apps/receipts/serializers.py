from rest_framework import serializers
from .models import ReceiptUpload


class ReceiptUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptUpload
        fields = [
            "id",
            "household",
            "uploaded_by",
            "file",
            "status",
            "raw_text",
            "extracted_data",
            "error_message",
            "created_at",
            "processed_at",
        ]
        read_only_fields = [
            "uploaded_by",
            "status",
            "raw_text",
            "extracted_data",
            "error_message",
            "created_at",
            "processed_at",
        ]