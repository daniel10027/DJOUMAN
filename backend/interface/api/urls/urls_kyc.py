from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.kyc_viewset import KycViewSet

router = DefaultRouter()
router.register("kyc", KycViewSet, basename="kyc")

urlpatterns = [path("", include(router.urls))]
