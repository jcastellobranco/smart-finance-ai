"""Read-side queries for the expenses domain."""
from django.db.models import Sum

from .models import Expense


def visible_expenses(user):
    return (
        Expense.objects.filter(household__members__user=user)
        .select_related("category", "paid_by", "household")
        .distinct()
    )


def expense_summary(user, household_id=None):
    queryset = visible_expenses(user)
    if household_id is not None:
        queryset = queryset.filter(household_id=household_id)

    by_category = list(
        queryset.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    total = queryset.aggregate(total=Sum("amount"))["total"] or 0
    return {"total": total, "by_category": by_category}
