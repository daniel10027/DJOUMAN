from dataclasses import dataclass
from core.application.dto.contract_dto import ContractCreateInput

@dataclass
class ContractUseCases:
    repo: "ContractRepositoryPort"

    def create(self, data: ContractCreateInput):
        return self.repo.create(**data.__dict__)
