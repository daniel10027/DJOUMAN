from rest_framework import viewsets, permissions, decorators, response, status, serializers as drf_serializers
from interface.api.serializers.device_serializers import DeviceRegisterSerializer
from infrastructure.persistence.repositories.device_repository import DeviceRepository
from drf_spectacular.utils import extend_schema

from interface.api.serializers.common import EmptySerializer


@extend_schema(tags=["Devices"])
class DeviceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    @decorators.action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        ser = DeviceRegisterSerializer(data=request.data); ser.is_valid(raise_exception=True)
        d = ser.validated_data
        obj = DeviceRepository().register(request.user.id, d["platform"], d["token"])
        return response.Response({"status": "ok", "token": obj.token})

    @decorators.action(detail=False, methods=["post"], url_path="unregister")
    def unregister(self, request):
        token = request.data.get("token")
        if not token: return response.Response({"error": "token required"}, status=400)
        DeviceRepository().unregister(token)
        return response.Response({"status": "ok"})
