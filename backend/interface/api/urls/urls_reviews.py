from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.review_viewset import ReviewViewSet

router = DefaultRouter()
router.register("reviews", ReviewViewSet, basename="reviews")

urlpatterns = [path("", include(router.urls))]