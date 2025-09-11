from dataclasses import dataclass

@dataclass(frozen=True)
class MissionActionInput:
    mission_id: int
    actor_id: int  # freelance id
