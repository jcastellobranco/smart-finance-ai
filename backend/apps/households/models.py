from django.conf import settings
from django.db import models


class Household(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_households",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HouseholdMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MEMBER = "member", "Member"

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="members",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="household_memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("household", "user")

    def __str__(self):
        return f"{self.user} - {self.household}"