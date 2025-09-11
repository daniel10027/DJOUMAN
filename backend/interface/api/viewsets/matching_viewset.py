from rest_framework import viewsets, permissions, decorators, response, serializers as drf_serializers
from interface.api.serializers.matching_serializers import MatchingQuerySerializer, MatchResultSerializer
from core.application.services.matching_service import find_freelancers
from drf_spectacular.utils import extend_schema
from rest_framework import status
from infrastructure.persistence.repositories.mission_repository import MissionRepository
from interface.api.serializers.common import EmptySerializer

@extend_schema(tags=["Matching"])
class MatchingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmptySerializer

    @decorators.action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        ser = MatchingQuerySerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        rs = find_freelancers(**ser.validated_data)
        return response.Response(MatchResultSerializer(rs, many=True).data)


    @decorators.action(detail=False, methods=["post"], url_path="assign", permission_classes=[permissions.IsAuthenticated])
    def assign(self, request):
        booking_id = int(request.data.get("booking_id", 0))
        freelance_id = int(request.data.get("freelance_id", 0))
        if not booking_id or not freelance_id:
            return response.Response({"error": "booking_id & freelance_id requis"}, status=400)
        m = MissionRepository().create_for_booking(booking_id, freelance_id)
        return response.Response({"mission_id": m.id}, status=status.HTTP_201_CREATED)
