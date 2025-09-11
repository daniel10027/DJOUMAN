from dataclasses import dataclass
from core.application.dto.equipment_dto import EquipmentCreateInput

@dataclass
class EquipmentUseCases:
    repo: "EquipmentRepositoryPort"

    def list(self, **filters):
        return self.repo.list(**filters)

    def create(self, data: EquipmentCreateInput):
        return self.repo.create(**data.__dict__)
