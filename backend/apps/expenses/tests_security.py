from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from apps.expenses.models import Expense
from apps.households.models import Household, HouseholdMember
from apps.receipts.models import ReceiptUpload
from apps.receipts.tasks import process_receipt_task


class FinancialIsolationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username="owner", password="safe-test-password")
        self.outsider = User.objects.create_user(username="outsider", password="safe-test-password")
        self.household = Household.objects.create(name="Private", owner=self.owner)
        HouseholdMember.objects.create(
            household=self.household, user=self.owner, role=HouseholdMember.Role.OWNER
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.outsider)

    def test_outsider_cannot_create_expense_for_other_household(self):
        response = self.client.post("/api/expenses/", {
            "household": self.household.pk,
            "description": "Unauthorized",
            "amount": "25.00",
            "expense_date": "2026-01-01",
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Expense.objects.exists())

    def test_outsider_cannot_upload_receipt_to_other_household(self):
        file = SimpleUploadedFile("receipt.pdf", b"%PDF-1.4\nexample", content_type="application/pdf")
        response = self.client.post("/api/receipts/", {
            "household": self.household.pk, "file": file,
        }, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ReceiptUpload.objects.exists())

    def test_invalid_receipt_content_is_rejected(self):
        self.client.force_authenticate(user=self.owner)
        file = SimpleUploadedFile("receipt.pdf", b"not a pdf", content_type="application/pdf")
        response = self.client.post("/api/receipts/", {
            "household": self.household.pk, "file": file,
        }, format="multipart")
        self.assertEqual(response.status_code, 400)

    @patch("apps.receipts.tasks.extract_receipt")
    def test_receipt_processing_is_idempotent(self, extractor):
        from apps.receipts.extraction import ExtractionResult
        extractor.return_value = ExtractionResult(raw_text="receipt", fields={
            "merchant": "Store", "description": "Groceries", "amount": "25.00",
            "date": str(date.today()), "category": "Groceries",
        })
        receipt = ReceiptUpload.objects.create(
            household=self.household, uploaded_by=self.owner,
            file="receipts/example.pdf",
        )
        process_receipt_task(receipt.pk)
        process_receipt_task(receipt.pk)
        self.assertEqual(Expense.objects.filter(receipt_upload=receipt).count(), 0)
        receipt.refresh_from_db()
        self.assertEqual(receipt.status, ReceiptUpload.Status.REVIEW)
