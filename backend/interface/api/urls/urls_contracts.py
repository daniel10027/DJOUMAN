from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.contract_viewset import ContractViewSet

router = DefaultRouter()
router.register("contracts", ContractViewSet, basename="contracts")

urlpatterns = [path("", include(router.urls))]