from dataclasses import dataclass
from core.application.dto.dispute_dto import DisputeCreateInput

@dataclass
class DisputeUseCases:
    repo: "DisputeRepositoryPort"

    def create(self, data: DisputeCreateInput):
        return self.repo.create(**data.__dict__)
