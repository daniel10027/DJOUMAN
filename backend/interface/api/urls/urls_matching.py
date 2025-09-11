from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.matching_viewset import MatchingViewSet

router = DefaultRouter()
router.register("matching", MatchingViewSet, basename="matching")

urlpatterns = [path("", include(router.urls))]
