from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.organization_viewset import OrganizationViewSet

router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organizations")

urlpatterns = [path("", include(router.urls))]
