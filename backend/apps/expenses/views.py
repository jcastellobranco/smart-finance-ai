from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .selectors import expense_summary, visible_expenses
from .serializers import ExpenseSerializer
from .services import create_expense


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return visible_expenses(self.request.user)

    def perform_create(self, serializer):
        create_expense(serializer=serializer, user=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        household_id = request.query_params.get("household")
        if household_id is not None:
            try:
                household_id = int(household_id)
                if household_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                raise ValidationError({"household": "Must be a positive integer."})
        return Response(expense_summary(request.user, household_id))
