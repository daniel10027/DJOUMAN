from django.urls import path, include

urlpatterns = [
    path("", include("interface.api.urls.urls_auth")),
    path("", include("interface.api.urls.urls_users")),
    path("", include("interface.api.urls.urls_catalog")),
    path("", include("interface.api.urls.urls_equipments")),
    path("", include("interface.api.urls.urls_bookings")),
    path("", include("interface.api.urls.urls_missions")),
    path("", include("interface.api.urls.urls_payments")),
    path("", include("interface.api.urls.urls_payouts")),
    path("", include("interface.api.urls.urls_contracts")),
    path("", include("interface.api.urls.urls_disputes")),
    path("", include("interface.api.urls.urls_reviews")),
    path("", include("interface.api.urls.urls_storage")),
    path("", include("interface.api.urls.urls_notifications")),
    path("", include("interface.api.urls.urls_commissions")),
    path("", include("interface.api.urls.urls_organizations")),
    path("", include("interface.api.urls.urls_kyc")),
    path("", include("interface.api.urls.urls_matching")),
    path("", include("interface.api.urls.urls_reports")),
    path("", include("interface.api.urls.urls_devices")),
]