from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import OwnerOrReadOnly
from .selectors import visible_households
from .serializers import HouseholdSerializer
from .services import create_household


class HouseholdViewSet(viewsets.ModelViewSet):
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]

    def get_queryset(self):
        return visible_households(self.request.user)

    def perform_create(self, serializer):
        create_household(serializer=serializer, user=self.request.user)
