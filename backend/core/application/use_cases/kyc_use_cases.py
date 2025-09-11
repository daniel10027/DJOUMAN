from dataclasses import dataclass

@dataclass
class KycUseCases:
    repo: "KycRepository"

    def submit(self, *, user_id: int, doc_type: str, file_url: str, data: dict | None = None):
        return self.repo.create(user_id=user_id, doc_type=doc_type, file_url=file_url, data=data or {})

    def approve(self, *, kyc_id: int, reviewer_id: int):
        kyc = self.repo.get(kyc_id)
        return self.repo.approve(kyc, reviewer_id)

    def reject(self, *, kyc_id: int, reviewer_id: int):
        kyc = self.repo.get(kyc_id)
        return self.repo.reject(kyc, reviewer_id)
