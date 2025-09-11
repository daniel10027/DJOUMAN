from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.mission_viewset import MissionViewSet

router = DefaultRouter()
router.register("missions", MissionViewSet, basename="missions")

urlpatterns = [path("", include(router.urls))]