from rest_framework import viewsets, permissions, decorators, response, serializers as drf_serializers
from core.application.services.report_service import kpis
from interface.api.serializers.report_serializers import KPISerializer
from infrastructure.security.permissions import IsAdmin
from drf_spectacular.utils import extend_schema
from interface.api.serializers.common import EmptySerializer

@extend_schema(tags=["Reports"])
class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAdmin]
    serializer_class = EmptySerializer

    @decorators.action(detail=False, methods=["get"], url_path="kpis")
    def dashboard_kpis(self, request):
        data = kpis()
        return response.Response(KPISerializer(data).data)
