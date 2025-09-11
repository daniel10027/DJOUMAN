from rest_framework import viewsets, mixins
from infrastructure.persistence.models import CommissionPolicy
from interface.api.serializers.commission_serializers import CommissionPolicySerializer
from infrastructure.security.permissions import AdminOrReadOnly
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["CommissionPolicy"])
class CommissionPolicyViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    queryset = CommissionPolicy.objects.select_related("service_category").all().order_by("id")
    serializer_class = CommissionPolicySerializer
    permission_classes = [AdminOrReadOnly]
