from dataclasses import dataclass
from core.application.dto.catalog_dto import CategoryCreateInput, ServiceCreateInput

@dataclass
class CatalogUseCases:
    repo: "CatalogRepositoryPort"

    # Categories
    def list_categories(self):
        return self.repo.list_categories()

    def create_category(self, data: CategoryCreateInput):
        return self.repo.create_category(name=data.name, slug=data.slug, is_active=data.is_active)

    # Services
    def list_services(self, **filters):
        return self.repo.list_services(**filters)

    def create_service(self, data: ServiceCreateInput):
        return self.repo.create_service(
            category_id=data.category_id,
            owner_id=data.owner_id,
            title=data.title,
            description=data.description,
            base_price=data.base_price,
            currency=data.currency,
            is_active=data.is_active,
        )
