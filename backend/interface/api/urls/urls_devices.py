from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.device_viewset import DeviceViewSet

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="devices")

urlpatterns = [path("", include(router.urls))]
