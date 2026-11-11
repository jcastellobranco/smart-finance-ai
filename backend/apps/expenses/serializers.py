from rest_framework import serializers
from apps.households.models import Household
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
            "id", "household", "paid_by", "category", "category_name",
            "description", "merchant", "amount", "expense_date", "source", "created_at",
        ]
        read_only_fields = ["paid_by", "source", "created_at"]

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

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
