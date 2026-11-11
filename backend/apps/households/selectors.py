"""Household access rules shared across application services."""
from .models import Household


def visible_households(user):
    return Household.objects.filter(members__user=user).distinct()


def is_household_owner(user, household):
    return household.owner_id == user.pk
