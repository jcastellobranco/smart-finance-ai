from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(
            household__members__user=self.request.user
        ).select_related("category", "paid_by", "household").distinct()

    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        queryset = self.get_queryset()

        by_category = (
            queryset
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        total = queryset.aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "total": total,
            "by_category": by_category,
        })