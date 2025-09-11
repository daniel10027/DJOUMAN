from rest_framework import viewsets, mixins, permissions
from infrastructure.persistence.models import ServiceCategory, Service
from interface.api.serializers.catalog_serializers import ServiceCategorySerializer, ServiceSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Category"])
class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ServiceCategory.objects.all().order_by("id")
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema(tags=["Service"])
class ServiceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Service.objects.select_related("category","owner").all().order_by("-id")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
