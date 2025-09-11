from dataclasses import dataclass

@dataclass(frozen=True)
class CategoryCreateInput:
    name: str
    slug: str
    is_active: bool = True

@dataclass(frozen=True)
class ServiceCreateInput:
    category_id: int
    owner_id: int
    title: str
    description: str | None = None
    base_price: float = 0.0
    currency: str = "XOF"
    is_active: bool = True
