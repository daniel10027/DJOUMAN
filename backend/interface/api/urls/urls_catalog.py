from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.catalog_viewset import CategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("services", ServiceViewSet, basename="services")

urlpatterns = [path("", include(router.urls))]
