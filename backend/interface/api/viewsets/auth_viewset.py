from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.application.use_cases.auth_use_cases import AuthUseCases
from core.application.dto.auth_dto import RegisterInput
from infrastructure.persistence.repositories.user_repository import UserRepository
from interface.api.serializers.auth_serializers import (
    RegisterSerializer, LoginSerializer,
    OTPRequestSerializer, OTPVerifySerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
)
from drf_spectacular.utils import extend_schema
from infrastructure.persistence.models import UserRole
from infrastructure.persistence.models.auth_otp import AuthOTP
from infrastructure.providers.notifications.factory import NotificationFacade
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework import serializers as drf_serializers
from rest_framework.permissions import AllowAny

from interface.api.serializers.common import EmptySerializer


@extend_schema(tags=["Authentication"])
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    allow_post_without_auth = True
    usecases = AuthUseCases(user_repo=UserRepository())
    serializer_class = EmptySerializer

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        out = self.usecases.register(RegisterInput(**ser.validated_data))
        return Response({"access": out.access, "refresh": out.refresh}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        out = self.usecases.login(ser.validated_data["identifier"], ser.validated_data["password"])
        if not out:
            return Response({"code": "invalid_credentials", "message": "Identifiants invalides."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"access": out.access, "refresh": out.refresh})

    @action(detail=False, methods=["post"], url_path="otp/request")
    def otp_request(self, request):
        ser = OTPRequestSerializer(data=request.data);
        ser.is_valid(raise_exception=True)
        ident = ser.validated_data["identifier"]
        User = get_user_model()
        try:
            user = User.objects.get(email=ident) if "@" in ident else User.objects.get(username=ident)
        except User.DoesNotExist:
            return Response({"error": "user_not_found"}, status=404)
        otp = AuthOTP.create_for(user.id, purpose="login")
        # envoie via email/sms (simple)
        if user.email:
            html = render_to_string("notifications/otp.html", {"code": otp.code, "user": user})
            NotificationFacade().email.send_email(user.email, "Votre code OTP", html)

        if user.phone:
            NotificationFacade().sms.send_sms(user.phone, f"Code OTP: {otp.code}")
        return Response({"status": "sent"})

    @action(detail=False, methods=["post"], url_path="otp/verify")
    def otp_verify(self, request):
        ser = OTPVerifySerializer(data=request.data);
        ser.is_valid(raise_exception=True)
        ident, code = ser.validated_data["identifier"], ser.validated_data["code"]
        User = get_user_model()
        try:
            user = User.objects.get(email=ident) if "@" in ident else User.objects.get(username=ident)
        except User.DoesNotExist:
            return Response({"error": "user_not_found"}, status=404)
        from django.utils import timezone
        otp = AuthOTP.objects.filter(user_id=user.id, code=code, purpose="login",
                                     expires_at__gte=timezone.now()).order_by("-id").first()
        if not otp:
            return Response({"error": "invalid_code"}, status=400)
        out = self.usecases.login(user.username, request.data.get("password", "") or user.password)  # bypass pw check
        # génère tokens JWT classiques
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})

    @action(detail=False, methods=["post"], url_path="password/reset-request")
    def password_reset_request(self, request):
        ser = PasswordResetRequestSerializer(data=request.data);
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status": "ok"})  # ne pas divulguer
        signer = TimestampSigner()
        token = signer.sign(user.pk)
        link = f"{request.build_absolute_uri('/')}reset?token={token}"
        html = render_to_string(
            "notifications/password_reset.html",
            {"link": link, "user": user, "support_email": "support@djouman.local", "now": now()},
        )
        NotificationFacade().email.send_email(email, "Réinitialiser votre mot de passe", html)
        return Response({"status": "ok"})

    @action(detail=False, methods=["post"], url_path="password/reset-confirm")
    def password_reset_confirm(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data["token"]
        new_pw = ser.validated_data["new_password"]
        from django.contrib.auth import get_user_model
        User = get_user_model()
        signer = TimestampSigner()
        try:
            user_id = signer.unsign(token, max_age=3600)
            user = User.objects.get(pk=user_id)
            user.set_password(new_pw);
            user.save(update_fields=["password"])
            return Response({"status": "ok"})
        except (BadSignature, SignatureExpired, User.DoesNotExist):
            return Response({"error": "invalid_or_expired"}, status=400)
