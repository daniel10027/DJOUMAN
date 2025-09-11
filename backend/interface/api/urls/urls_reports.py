from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interface.api.viewsets.report_viewset import ReportViewSet

router = DefaultRouter()
router.register("reports", ReportViewSet, basename="reports")

urlpatterns = [path("", include(router.urls))]
