from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("interface.api.health_urls")),

    # Global
    path("api/schema/", SpectacularAPIView.as_view(urlconf=None), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),

    path("api/v1/", include("interface.api.routers")),
]

domains = [
    ("auth","urls_auth"), ("users","urls_users"), ("catalog","urls_catalog"),
    ("equipments","urls_equipments"), ("bookings","urls_bookings"),
    ("missions","urls_missions"), ("payments","urls_payments"),
    ("payouts","urls_payouts"), ("contracts","urls_contracts"),
    ("disputes","urls_disputes"), ("reviews","urls_reviews"),
    ("storage","urls_storage"), ("notifications","urls_notifications"),
    ("kyc","urls_kyc"), ("devices","urls_devices"),
    ("organizations","urls_organizations"), ("commissions","urls_commissions"),
    ("matching","urls_matching"), ("reports","urls_reports"),
]
for name, mod in domains:
    urlpatterns += [
        path(f"api/schema/{name}/", SpectacularAPIView.as_view(urlconf=f"interface.api.urls.{mod}"), name=f"schema-{name}"),
        path(f"api/docs/{name}/",   SpectacularSwaggerView.as_view(url_name=f"schema-{name}"),      name=f"docs-{name}"),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("api/docs/logo.png", RedirectView.as_view(url=f"{settings.STATIC_URL}logo.png")),
]