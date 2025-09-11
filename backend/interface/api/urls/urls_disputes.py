from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.dispute_viewset import DisputeViewSet

router = DefaultRouter()
router.register("disputes", DisputeViewSet, basename="disputes")

urlpatterns = [path("", include(router.urls))]