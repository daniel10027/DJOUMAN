from infrastructure.persistence.models import ServiceCategory, Service

class CatalogRepository:
    # Categories
    def list_categories(self):
        return ServiceCategory.objects.filter(is_active=True).order_by("name")

    def create_category(self, **kwargs):
        return ServiceCategory.objects.create(**kwargs)

    # Services
    def list_services(self, **filters):
        qs = Service.objects.select_related("category","owner").filter(is_active=True)
        if "category" in filters:
            qs = qs.filter(category_id=filters["category"])
        if "owner" in filters:
            qs = qs.filter(owner_id=filters["owner"])
        return qs.order_by("-id")

    def create_service(self, **kwargs):
        return Service.objects.create(**kwargs)
