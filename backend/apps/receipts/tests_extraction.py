from decimal import Decimal
from django.test import SimpleTestCase
from apps.receipts.services import normalize_amount


class AmountNormalizationTests(SimpleTestCase):
    def test_brazilian_currency(self):
        self.assertEqual(normalize_amount("R$ 1.234,56"), Decimal("1234.56"))

    def test_decimal_currency(self):
        self.assertEqual(normalize_amount("12.50"), Decimal("12.50"))

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            normalize_amount("-1.00")
