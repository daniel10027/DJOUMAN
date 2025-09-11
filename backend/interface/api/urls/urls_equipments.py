from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.equipment_viewset import EquipmentViewSet

router = DefaultRouter()
router.register("equipments", EquipmentViewSet, basename="equipments")

urlpatterns = [path("", include(router.urls))]