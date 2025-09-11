from typing import Iterable
from infrastructure.persistence.models import Review

class ReviewRepository:
    def list(self, **filters) -> Iterable[Review]:
        qs = Review.objects.select_related("author", "target_user", "booking").all()
        if "author" in filters:
            qs = qs.filter(author_id=filters["author"])
        if "target_user" in filters:
            qs = qs.filter(target_user_id=filters["target_user"])
        if "booking" in filters:
            qs = qs.filter(booking_id=filters["booking"])
        if "min_rating" in filters:
            qs = qs.filter(rating__gte=filters["min_rating"])
        if "max_rating" in filters:
            qs = qs.filter(rating__lte=filters["max_rating"])
        return qs.order_by("-created_at")

    def get(self, review_id: int) -> Review:
        return Review.objects.get(pk=review_id)

    def create(self, **kwargs) -> Review:
        return Review.objects.create(**kwargs)

    def save(self, review: Review) -> Review:
        review.save()
        return review
