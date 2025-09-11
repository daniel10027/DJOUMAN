from rest_framework import viewsets, mixins, permissions
from interface.api.serializers.user_serializers import UserSerializer
from drf_spectacular.utils import extend_schema
from infrastructure.persistence.models import User

@extend_schema(tags=["Users"])
class MeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.none()

    @extend_schema(parameters=[])
    def get_object(self):
        return self.request.user
