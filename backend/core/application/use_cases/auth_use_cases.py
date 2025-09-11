from typing import Optional
from dataclasses import dataclass
from django.contrib.auth.hashers import make_password
from infrastructure.persistence.models import UserRole
from core.application.dto.auth_dto import RegisterInput, AuthOutput
from rest_framework_simplejwt.tokens import RefreshToken

@dataclass
class AuthUseCases:
    user_repo: "UserRepositoryPort"

    def register(self, data: RegisterInput) -> AuthOutput:
        role = data.role or UserRole.CLIENT
        user = self.user_repo.create_user(
            username=data.username,
            email=data.email,
            password=make_password(data.password),
            role=role,
            phone=data.phone,
        )
        self.user_repo.ensure_profile(user, name=data.name or data.username)
        refresh = RefreshToken.for_user(user)
        return AuthOutput(access=str(refresh.access_token), refresh=str(refresh))

    def login(self, identifier: str, password: str) -> Optional[AuthOutput]:
        user = self.user_repo.get_by_username_or_email(identifier)
        if not user or not user.check_password(password):
            return None
        refresh = RefreshToken.for_user(user)
        return AuthOutput(access=str(refresh.access_token), refresh=str(refresh))
