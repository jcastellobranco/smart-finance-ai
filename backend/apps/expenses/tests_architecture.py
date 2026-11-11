from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from apps.expenses.models import Expense
from apps.expenses.selectors import expense_summary
from apps.households.models import Household, HouseholdMember

class ModularArchitectureTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username="owner2", password="test-password")
        self.member = User.objects.create_user(username="member2", password="test-password")
        self.household = Household.objects.create(name="Family", owner=self.owner)
        for user, role in ((self.owner, HouseholdMember.Role.OWNER), (self.member, HouseholdMember.Role.MEMBER)):
            HouseholdMember.objects.create(household=self.household, user=user, role=role)
        self.client = APIClient()

    def test_member_cannot_update_household(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(f"/api/households/{self.household.pk}/", {"name": "Changed"})
        self.assertEqual(response.status_code, 403)

    def test_owner_can_update_household(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(f"/api/households/{self.household.pk}/", {"name": "Updated"})
        self.assertEqual(response.status_code, 200)

    def test_summary_selector_scopes_to_household(self):
        Expense.objects.create(household=self.household, paid_by=self.owner, description="Food", amount=Decimal("12.50"), expense_date="2026-01-01")
        result = expense_summary(self.owner, self.household.pk)
        self.assertEqual(result["total"], Decimal("12.50"))

    def test_summary_rejects_invalid_household_parameter(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get("/api/expenses/summary/?household=invalid")
        self.assertEqual(response.status_code, 400)
