from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.user_viewset import MeViewSet

router = DefaultRouter()
router.register("me", MeViewSet, basename="me")

urlpatterns = [path("", include(router.urls))]
