from rest_framework import viewsets, mixins, permissions
from infrastructure.persistence.models import Organization
from interface.api.serializers.organization_serializers import OrganizationSerializer
from infrastructure.security.permissions import AdminOrReadOnly
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Organization"])
class OrganizationViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Organization.objects.all().order_by("name")
    serializer_class = OrganizationSerializer
    permission_classes = [AdminOrReadOnly]
