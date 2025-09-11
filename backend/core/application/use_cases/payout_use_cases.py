from dataclasses import dataclass
from core.application.dto.payout_dto import PayoutCreateInput

@dataclass
class PayoutUseCases:
    repo: "PayoutRepositoryPort"

    def create(self, data: PayoutCreateInput):
        return self.repo.create(**data.__dict__)
