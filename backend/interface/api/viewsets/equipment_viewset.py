from rest_framework import viewsets, mixins, permissions
from infrastructure.persistence.models import Equipment
from interface.api.serializers.equipment_serializers import EquipmentSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Equipment"])
class EquipmentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Equipment.objects.select_related("owner").all().order_by("-id")
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
