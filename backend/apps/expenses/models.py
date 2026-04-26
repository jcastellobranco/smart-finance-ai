from django.conf import settings
from django.db import models

from apps.households.models import Household


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    class Source(models.TextChoices):
        MANUAL = "manual", "Manual"
        RECEIPT = "receipt", "Receipt"

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="paid_expenses",
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    description = models.CharField(max_length=255)
    merchant = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()

    source = models.CharField(
        max_length=30,
        choices=Source.choices,
        default=Source.MANUAL,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"