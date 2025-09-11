from typing import Iterable
from infrastructure.persistence.models import DeviceToken

class DeviceRepository:
    def list_by_user(self, user_id: int) -> Iterable[DeviceToken]:
        return DeviceToken.objects.filter(user_id=user_id).order_by("-last_seen_at")

    def register(self, user_id: int, platform: str, token: str) -> DeviceToken:
        obj, created = DeviceToken.objects.get_or_create(token=token, defaults={"user_id": user_id, "platform": platform})
        if not created and obj.user_id != user_id:
            obj.user_id = user_id
            obj.platform = platform
            obj.save(update_fields=["user","platform"])
        return obj

    def unregister(self, token: str) -> None:
        DeviceToken.objects.filter(token=token).delete()
