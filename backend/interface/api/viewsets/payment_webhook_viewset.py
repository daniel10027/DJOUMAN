from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiResponse
from infrastructure.persistence.models import PaymentStatus, Payment
from infrastructure.persistence.repositories.event_repository import EventRepository
from core.shared.utils import verify_hmac_signature
import stripe

class PaymentWebhookViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    events = EventRepository()

    def _ack(self): return Response({"ok": True}, status=status.HTTP_200_OK)

    def _process(self, source: str, request):

        # 1) signature
        secret = {
            "wave": getattr(settings, "WAVE_WEBHOOK_SECRET", ""),
            "stripe": getattr(settings, "STRIPE_WEBHOOK_SECRET", ""),
            "orange-money": getattr(settings, "OM_WEBHOOK_SECRET", ""),
            "mtn-momo": getattr(settings, "MTN_WEBHOOK_SECRET", ""),
        }.get(source, "")
        signature = request.headers.get("X-Signature") or request.headers.get("Stripe-Signature")
        raw = request.body or b""

        if secret and not verify_hmac_signature(raw, signature, secret):
            return Response({"error": "invalid signature"}, status=400)

        ref = request.data.get("provider_ref")
        event_id = request.data.get("event_id") or ref or ""
        if not ref:
            return Response({"error": "provider_ref required"}, status=400)

        if source == "stripe":
            try:
                payload = request.body.decode("utf-8")
                sig_header = request.headers.get("Stripe-Signature", "")
                stripe.Webhook.construct_event(payload, sig_header, getattr(settings, "STRIPE_WEBHOOK_SECRET", ""))
            except Exception:
                return Response({"error": "invalid signature"}, status=400)
        else:
            if secret and not verify_hmac_signature(raw, signature, secret):
                return Response({"error": "invalid signature"}, status=400)

        # 2) idempotence persistée
        ev, created = self.events.get_or_create_event(source, event_id, signature, payload=request.data)
        if not created and ev.status == "processed":
            return self._ack()

        # 3) appliquer statut
        status_value = request.data.get("status", PaymentStatus.SUCCEEDED)
        try:
            p = Payment.objects.get(provider_ref=ref)
            if p.status != status_value:
                p.status = status_value
                p.save(update_fields=["status"])
            self.events.mark_processed(ev)
        except Payment.DoesNotExist:
            self.events.mark_error(ev)
            return Response({"error": "unknown provider_ref"}, status=404)
        return self._ack()

    @extend_schema(tags=["Payment"], summary="Webhook Wave", request=None, responses={200: OpenApiResponse(description="OK")})
    @action(detail=False, methods=["post"], url_path="wave")
    def wave(self, request): return self._process("wave", request)

    @extend_schema(tags=["Payment"], summary="Webhook Stripe", request=None, responses={200: OpenApiResponse(description="OK")})
    @action(detail=False, methods=["post"], url_path="stripe")
    def stripe(self, request): return self._process("stripe", request)

    @extend_schema(tags=["Payment"], summary="Webhook Orange Money", request=None, responses={200: OpenApiResponse(description="OK")})
    @action(detail=False, methods=["post"], url_path="orange-money")
    def orange_money(self, request): return self._process("orange-money", request)

    @extend_schema(tags=["Payment"], summary="Webhook MTN MoMo", request=None, responses={200: OpenApiResponse(description="OK")})
    @action(detail=False, methods=["post"], url_path="mtn-momo")
    def mtn_momo(self, request): return self._process("mtn-momo", request)
