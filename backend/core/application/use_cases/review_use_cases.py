from dataclasses import dataclass
from core.application.dto.review_dto import ReviewCreateInput

@dataclass
class ReviewUseCases:
    repo: "ReviewRepositoryPort"

    def create(self, data: ReviewCreateInput):
        return self.repo.create(**data.__dict__)
