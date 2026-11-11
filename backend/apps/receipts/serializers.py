from pathlib import Path

from django.conf import settings
from rest_framework import serializers

from apps.households.models import Household
from .models import ReceiptUpload

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {
    ".pdf": {"application/pdf"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".png": {"image/png"},
    ".webp": {"image/webp"},
}


class ReceiptUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptUpload
        fields = [
            "id", "household", "uploaded_by", "file", "status",
            "raw_text", "extracted_data", "error_message", "created_at", "processed_at",
        ]
        read_only_fields = [
            "uploaded_by", "status", "raw_text", "extracted_data",
            "error_message", "created_at", "processed_at",
        ]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["household"].queryset = Household.objects.filter(
                members__user=request.user
            ).distinct()
        else:
            fields["household"].queryset = Household.objects.none()
        return fields

    def validate_file(self, value):
        max_bytes = getattr(settings, "RECEIPT_MAX_UPLOAD_BYTES", 10 * 1024 * 1024)
        if value.size > max_bytes or value.size == 0:
            raise serializers.ValidationError("Receipt must be between 1 byte and 10 MB.")

        extension = Path(value.name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError("Unsupported receipt file extension.")

        content_type = getattr(value, "content_type", "")
        if content_type not in ALLOWED_MIME_TYPES[extension]:
            raise serializers.ValidationError("Unsupported receipt content type.")

        position = value.tell()
        try:
            value.seek(0)
            header = value.read(16)
        finally:
            value.seek(position)

        signatures = {
            ".pdf": (b"%PDF-",),
            ".jpg": (b"\xff\xd8\xff",),
            ".jpeg": (b"\xff\xd8\xff",),
            ".png": (b"\x89PNG\r\n\x1a\n",),
            ".webp": (b"RIFF",),
        }
        if not any(header.startswith(signature) for signature in signatures[extension]):
            raise serializers.ValidationError("File content does not match its extension.")
        if extension == ".webp" and header[8:12] != b"WEBP":
            raise serializers.ValidationError("Invalid WebP header.")
        return value
