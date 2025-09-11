from rest_framework import viewsets, mixins, permissions, decorators, response, status
from interface.api.serializers.payment_serializers import PaymentIntentSerializer, PaymentSerializer
from infrastructure.persistence.models import Payment
from core.application.use_cases.payment_use_cases import PaymentUseCases
from core.application.dto.payment_dto import PaymentIntentInput, RefundInput
from infrastructure.persistence.repositories.payment_repository import PaymentRepository
from infrastructure.providers.payments.factory import get_payment_provider
from infrastructure.persistence.repositories.payment_repository import PaymentRepository
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Payment"])
class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.select_related("booking").all().order_by("-id")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _uc_for_method(self, method: str):
        return PaymentUseCases(repo=PaymentRepository(), provider=get_payment_provider(method))

    def _uc_for_payment_id(self, payment_id: int):
        p = PaymentRepository().get(payment_id)
        return PaymentUseCases(repo=PaymentRepository(), provider=get_payment_provider(p.method))

    @decorators.action(detail=False, methods=["post"], url_path="intents")
    def create_intent(self, request):
        ser = PaymentIntentSerializer(data=request.data);
        ser.is_valid(raise_exception=True)
        uc = self._uc_for_method(ser.validated_data["method"])
        obj = uc.create_intent(PaymentIntentInput(**ser.validated_data))
        return response.Response(PaymentSerializer(obj).data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=["post"], url_path="capture")
    def capture(self, request, pk=None):
        uc = self._uc_for_payment_id(int(pk))
        obj = uc.capture(int(pk))
        return response.Response(PaymentSerializer(obj).data)

    @decorators.action(detail=True, methods=["post"], url_path="refund")
    def refund(self, request, pk=None):
        uc = self._uc_for_payment_id(int(pk))
        amount = request.data.get("amount")
        obj = uc.refund(RefundInput(payment_id=int(pk), amount=amount))
        return response.Response(PaymentSerializer(obj).data)