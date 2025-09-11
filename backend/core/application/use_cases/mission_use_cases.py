from dataclasses import dataclass
from infrastructure.persistence.models import MissionStatus
from django.utils import timezone

@dataclass
class MissionUseCases:
    repo: "MissionRepositoryPort"

    def start(self, mission_id: int, actor_id: int):
        m = self.repo.get(mission_id)
        if m.freelance_id != actor_id:
            raise PermissionError("Not mission owner")
        m.status = MissionStatus.STARTED
        m.started_at = timezone.now()
        return self.repo.save(m)

    def pause(self, mission_id: int, actor_id: int):
        m = self.repo.get(mission_id)
        if m.freelance_id != actor_id:
            raise PermissionError("Not mission owner")
        m.status = MissionStatus.PAUSED
        m.paused_at = timezone.now()
        return self.repo.save(m)

    def stop(self, mission_id: int, actor_id: int):
        m = self.repo.get(mission_id)
        if m.freelance_id != actor_id:
            raise PermissionError("Not mission owner")
        m.status = MissionStatus.STOPPED
        m.stopped_at = timezone.now()
        return self.repo.save(m)

    def complete(self, mission_id: int, actor_id: int):
        m = self.repo.get(mission_id)
        if m.freelance_id != actor_id:
            raise PermissionError("Not mission owner")
        m.status = MissionStatus.COMPLETED
        m.completed_at = timezone.now()
        return self.repo.save(m)