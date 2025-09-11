from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewCreateInput:
    author_id: int
    target_user_id: int
    booking_id: int | None
    rating: int
    comment: str | None = None
