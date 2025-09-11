from rest_framework import viewsets, mixins, permissions, decorators, response
from interface.api.serializers.dispute_serializers import DisputeSerializer
from infrastructure.persistence.models import Dispute, DisputeStatus
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Dispute"])
class DisputeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Dispute.objects.select_related("booking","opener").all().order_by("-id")
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(opener=self.request.user)

    @extend_schema(tags=["Dispute"], summary="Ajouter un message à un litige", request=None, responses={200: DisputeSerializer})
    @decorators.action(detail=True, methods=["post"], url_path="add-message")
    def add_message(self, request, pk=None):
        d = self.get_object()
        msg = request.data or {}
        msgs = list(d.messages or [])
        msgs.append({"author_id": request.user.id, **msg})
        d.messages = msgs
        d.save(update_fields=["messages"])
        return response.Response(DisputeSerializer(d).data)

    @extend_schema(tags=["Dispute"], summary="Changer le statut", request=None, responses={200: DisputeSerializer})
    @decorators.action(detail=True, methods=["post"], url_path="set-status")
    def set_status(self, request, pk=None):
        d = self.get_object()
        status_value = request.data.get("status")
        if status_value not in DisputeStatus.values:
            return response.Response({"error": "invalid status"}, status=400)
        d.status = status_value
        d.save(update_fields=["status"])
        return response.Response(DisputeSerializer(d).data)