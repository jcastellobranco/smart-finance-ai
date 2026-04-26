from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from apps.households.models import Household, HouseholdMember

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    households = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "households"]

    def get_households(self, user):
        memberships = (
            HouseholdMember.objects
            .filter(user=user)
            .select_related("household")
            .order_by("household__name")
        )

        return [
            {
                "id": membership.household_id,
                "name": membership.household.name,
                "role": membership.role,
            }
            for membership in memberships
        ]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    household_name = serializers.CharField(max_length=120, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")

        return value

    def create(self, validated_data):
        household_name = validated_data.pop("household_name", "")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        household = Household.objects.create(
            name=household_name or f"{user.username}'s household",
            owner=user,
        )
        HouseholdMember.objects.create(
            household=household,
            user=user,
            role=HouseholdMember.Role.OWNER,
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        attrs["user"] = user
        return attrs
