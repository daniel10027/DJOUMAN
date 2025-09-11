from typing import Optional
from infrastructure.persistence.models import User, Profile

class UserRepository:
    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        try:
            return User.objects.filter(is_active=True).get(
                **({"email": identifier} if "@" in identifier else {"username": identifier})
            )
        except User.DoesNotExist:
            return None

    def create_user(self, **kwargs) -> User:
        return User.objects.create(**kwargs)

    def ensure_profile(self, user: User, **kwargs) -> Profile:
        profile, created = Profile.objects.get_or_create(user=user, defaults=kwargs)
        if not created and kwargs:
            for k, v in kwargs.items():
                setattr(profile, k, v)
            profile.save(update_fields=list(kwargs.keys()))
        return profile

    def get(self, user_id: int) -> User:
        return User.objects.get(pk=user_id)
