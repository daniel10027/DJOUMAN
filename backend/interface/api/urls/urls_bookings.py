from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.booking_viewset import BookingViewSet

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="bookings")

urlpatterns = [path("", include(router.urls))]