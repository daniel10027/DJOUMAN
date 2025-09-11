from rest_framework import viewsets, mixins, permissions, decorators, response, status
from interface.api.serializers.contract_serializers import ContractSerializer
from infrastructure.persistence.models import Contract
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from infrastructure.providers.pdf.factory import get_pdf_port

@extend_schema(tags=["Contract"])
class ContractViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Contract.objects.select_related("booking").all().order_by("-id")
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Contract"], summary="Générer et associer un contrat PDF à un booking",
        request=None,
        responses={201: ContractSerializer, 400: OpenApiResponse(description="Validation error")},
        examples=[OpenApiExample("GenerateContractPayload", value={"booking_id": 123, "context": {"client": "Alice"}}, request_only=True)],
    )
    @decorators.action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        booking_id = request.data.get("booking_id")
        context = request.data.get("context", {})
        if not booking_id:
            return response.Response({"error": "booking_id required"}, status=status.HTTP_400_BAD_REQUEST)
        pdf = get_pdf_port()
        file_url = pdf.render_contract(booking_id=int(booking_id), context=context)
        obj = Contract.objects.create(booking_id=booking_id, file_url=file_url)
        return response.Response(ContractSerializer(obj).data, status=status.HTTP_201_CREATED)
