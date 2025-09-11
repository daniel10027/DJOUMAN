from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.payment_viewset import PaymentViewSet
from interface.api.viewsets.payment_webhook_viewset import PaymentWebhookViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")
router.register("payments/webhooks", PaymentWebhookViewSet, basename="payment-webhooks")

urlpatterns = [path("", include(router.urls))]