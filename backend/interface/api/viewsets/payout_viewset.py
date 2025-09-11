from rest_framework import viewsets, mixins, permissions
from interface.api.serializers.payout_serializers import PayoutSerializer
from infrastructure.persistence.models import Payout

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Payout"])
class PayoutViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Payout.objects.select_related("beneficiary").all().order_by("-id")
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(beneficiary=self.request.user)
