from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.storage_viewset import StorageViewSet

router = DefaultRouter()
router.register("storage", StorageViewSet, basename="storage")

urlpatterns = [path("", include(router.urls))]