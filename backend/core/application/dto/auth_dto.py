from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterInput:
    username: str
    email: str
    password: str
    role: str | None = None
    phone: str | None = None
    name: str | None = None

@dataclass(frozen=True)
class AuthOutput:
    access: str
    refresh: str
