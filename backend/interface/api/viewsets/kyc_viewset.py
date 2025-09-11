from rest_framework import viewsets, mixins, decorators, response, status, permissions
from interface.api.serializers.kyc_serializers import KycSerializer
from infrastructure.persistence.models import KycDocument, KycStatus
from core.application.use_cases.kyc_use_cases import KycUseCases
from infrastructure.persistence.repositories.kyc_repository import KycRepository
from drf_spectacular.utils import extend_schema
from infrastructure.security.permissions import IsAdmin

@extend_schema(tags=["KYC"])
class KycViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = KycDocument.objects.select_related("user","reviewed_by").all().order_by("-id")
    serializer_class = KycSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.action(detail=True, methods=["post"], url_path="approve", permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        uc = KycUseCases(repo=KycRepository())
        obj = uc.approve(kyc_id=int(pk), reviewer_id=request.user.id)
        return response.Response(KycSerializer(obj).data)

    @decorators.action(detail=True, methods=["post"], url_path="reject", permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        uc = KycUseCases(repo=KycRepository())
        obj = uc.reject(kyc_id=int(pk), reviewer_id=request.user.id)
        return response.Response(KycSerializer(obj).data)
