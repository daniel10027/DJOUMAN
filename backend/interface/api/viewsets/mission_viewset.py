from rest_framework import viewsets, mixins, permissions, decorators, response
from infrastructure.persistence.models import Mission
from interface.api.serializers.mission_serializers import MissionSerializer
from core.application.use_cases.mission_use_cases import MissionUseCases
from infrastructure.persistence.repositories.mission_repository import MissionRepository
import logging
from infrastructure.providers.notifications.factory import NotificationFacade

logger = logging.getLogger(__name__)
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Mission"])
class MissionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Mission.objects.select_related("booking","freelance").all().order_by("-id")
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_repo(self):
        return MissionRepository()

    @decorators.action(detail=True, methods=["post"], url_path="start")
    def start(self, request, pk=None):
        uc = MissionUseCases(repo=self.get_repo())
        m = uc.start(int(pk), request.user.id)
        try:
            NotificationFacade().notify_mission_status(m.freelance_id, m.id, m.status)
        except Exception:
            logger.exception("Mission start notification failed")
        return response.Response(MissionSerializer(m).data)

    @decorators.action(detail=True, methods=["post"], url_path="pause")
    def pause(self, request, pk=None):
        uc = MissionUseCases(repo=self.get_repo())
        m = uc.pause(int(pk), request.user.id)
        try:
            NotificationFacade().notify_mission_status(m.freelance_id, m.id, m.status)
        except Exception:
            logger.exception("Mission pause notification failed")
        return response.Response(MissionSerializer(m).data)

    @decorators.action(detail=True, methods=["post"], url_path="stop")
    def stop(self, request, pk=None):
        uc = MissionUseCases(repo=self.get_repo())
        m = uc.stop(int(pk), request.user.id)
        try:
            NotificationFacade().notify_mission_status(m.freelance_id, m.id, m.status)
        except Exception:
            logger.exception("Mission stop notification failed")
        return response.Response(MissionSerializer(m).data)

    @decorators.action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        uc = MissionUseCases(repo=self.get_repo())
        m = uc.complete(int(pk), request.user.id)
        try:
            NotificationFacade().notify_mission_status(m.freelance_id, m.id, m.status)
        except Exception:
            logger.exception("Mission complete notification failed")
        return response.Response(MissionSerializer(m).data)

