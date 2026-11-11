"""Household write-side application services."""
from django.db import transaction

from .models import HouseholdMember


@transaction.atomic
def create_household(*, serializer, user):
    household = serializer.save(owner=user)
    HouseholdMember.objects.create(
        household=household, user=user, role=HouseholdMember.Role.OWNER
    )
    return household
