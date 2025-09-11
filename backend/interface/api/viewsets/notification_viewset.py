import logging
from rest_framework import viewsets, permissions, decorators, response, status
from drf_spectacular.utils import (
    extend_schema, OpenApiResponse, OpenApiExample
)
from interface.api.serializers.notification_serializers import (
    PushNotificationSerializer, EmailNotificationSerializer,
    SmsNotificationSerializer, NotificationResponseSerializer
)
from infrastructure.providers.notifications.factory import NotificationFacade

logger = logging.getLogger(__name__)

@extend_schema(tags=["Notifications"])
class NotificationViewSet(viewsets.ViewSet):
    """
    Endpoints utilitaires pour envoyer des notifications:
    - POST /notifications/push
    - POST /notifications/email
    - POST /notifications/sms
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Envoyer une notification push à un utilisateur",
        request=PushNotificationSerializer,
        responses={200: OpenApiResponse(response=NotificationResponseSerializer, description="Push envoyé")},
        examples=[
            OpenApiExample(
                "PushExample",
                value={"user_id": 42, "title": "Réservation confirmée", "body": "Votre réservation #123 est confirmée", "data": {"booking_id": "123"}},
                request_only=True,
            )
        ],
    )
    @decorators.action(detail=False, methods=["post"], url_path="push")
    def push(self, request):
        ser = PushNotificationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            NotificationFacade().push.send_push(d["user_id"], d["title"], d["body"], d.get("data"))
        except Exception:
            logger.exception("Push send failed")
            return response.Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({"status": "sent"})

    @extend_schema(
        summary="Envoyer un e-mail",
        request=EmailNotificationSerializer,
        responses={200: OpenApiResponse(response=NotificationResponseSerializer, description="Email envoyé")},
        examples=[
            OpenApiExample(
                "EmailExample",
                value={"to": "alice@test.com", "subject": "Bienvenue", "html": "<h1>Bienvenue sur Djouman</h1>"},
                request_only=True,
            )
        ],
    )
    @decorators.action(detail=False, methods=["post"], url_path="email")
    def email(self, request):
        ser = EmailNotificationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            NotificationFacade().email.send_email(d["to"], d["subject"], d["html"])
        except Exception:
            logger.exception("Email send failed")
            return response.Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({"status": "sent"})

    @extend_schema(
        summary="Envoyer un SMS",
        request=SmsNotificationSerializer,
        responses={200: OpenApiResponse(response=NotificationResponseSerializer, description="SMS envoyé")},
        examples=[OpenApiExample("SmsExample", value={"to": "+2250700000000", "message": "Code OTP: 123456"}, request_only=True)],
    )
    @decorators.action(detail=False, methods=["post"], url_path="sms")
    def sms(self, request):
        ser = SmsNotificationSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            NotificationFacade().sms.send_sms(d["to"], d["message"])
        except Exception:
            logger.exception("SMS send failed")
            return response.Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({"status": "sent"})
