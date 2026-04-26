from rest_framework import serializers
from .models import Expense, ExpenseCategory


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "household",
            "paid_by",
            "category",
            "category_name",
            "description",
            "merchant",
            "amount",
            "expense_date",
            "source",
            "created_at",
        ]
        read_only_fields = ["paid_by", "source", "created_at"]