"""Write-side operations for the expenses domain."""
from django.db import transaction


@transaction.atomic
def create_expense(*, serializer, user):
    return serializer.save(paid_by=user)
