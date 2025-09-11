from rest_framework import viewsets, mixins, permissions, decorators, response, status
from infrastructure.persistence.models import Booking
from interface.api.serializers.booking_serializers import BookingSerializer
from core.application.use_cases.booking_use_cases import BookingUseCases
from infrastructure.persistence.repositories.booking_repository import BookingRepository
from core.application.services.pricing_service import compute_booking_price
from core.application.services.commission_service import compute_commission
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
import logging
from infrastructure.providers.notifications.factory import NotificationFacade

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(tags=["Booking"], summary="Lister les réservations", responses={200: BookingSerializer}),
    create=extend_schema(
        tags=["Booking"], summary="Créer une réservation",
        request=BookingSerializer,
        responses={201: OpenApiResponse(response=BookingSerializer, description="Réservation créée"), 400: OpenApiResponse(description="Erreur de validation")},
        examples=[OpenApiExample(
            "CreateBookingPayload",
            value={
                "service": 1,
                "equipment": None,
                "start_at": "2025-09-11T10:00:00Z",
                "end_at": "2025-09-12T12:00:00Z",
                "location_lat": 5.345678, "location_lng": -4.012345
            }, request_only=True
        )],
    ),
)

@extend_schema(tags=["Booking"])
class BookingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.select_related("client","service","equipment").all().order_by("-id")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        obj = serializer.save(client=user)
        # days calculés
        days = BookingSerializer.compute_days(obj.start_at, obj.end_at)
        base = float(obj.service.base_price) if obj.service_id else float(obj.equipment.price_per_day)
        price = compute_booking_price(base=base, days=days)
        rate, com = compute_commission(obj.service, amount=price)
        obj.price = price
        obj.commission_rate = rate
        obj.commission_amount = com
        obj.save(update_fields=["price","commission_rate","commission_amount"])

    @decorators.action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        uc = BookingUseCases(bookings=BookingRepository())
        b = uc.confirm(int(pk))

        # Notifications (MVP)
        try:
            NotificationFacade().notify_booking_confirmed(b.client_id, b.id)
        except Exception:
            logger.exception("Booking confirm notification failed")

        return response.Response(BookingSerializer(b).data)

    @decorators.action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, pk=None):
        uc = BookingUseCases(bookings=BookingRepository())
        b = uc.cancel(int(pk))
        return response.Response(BookingSerializer(b).data, status=status.HTTP_200_OK)
