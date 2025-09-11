from typing import Protocol

class StoragePort(Protocol):
    def presign_upload(self, *, path: str, content_type: str, expires: int = 3600) -> dict: ...
