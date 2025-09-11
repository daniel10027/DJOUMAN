from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.commission_viewset import CommissionPolicyViewSet

router = DefaultRouter()
router.register("commissions", CommissionPolicyViewSet, basename="commissions")

urlpatterns = [path("", include(router.urls))]
