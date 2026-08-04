from datetime import datetime
from typing import ClassVar

from core.constants import (
    ALLOWED_EMAIL_DOMAINS,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

from .base import ResponseBase

# class UserBase(BaseModel):
#     user_name: str | None = Field(default=None, max_length=USERNAME_MAX_LENGTH)

#     # a user should not have a name, when user logins or register he enter email and password
#     @field_validator("user_name")
#     @classmethod
#     def validate_name(cls, name: str | None) -> None | str:
#         if name is not None and not re.match(r"^[A-Za-z\s\-']+$", name):
#             raise ValueError("invalid user name")
#         return name


class UserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: SecretStr = Field(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )

    # what is mode here? should I write this validate email domain method above password field?
    @field_validator("email", mode="before")
    @classmethod
    def validate_email_domain(cls, email: str) -> str:
        domain: str = email.split("@")[-1].lower()
        if domain not in ALLOWED_EMAIL_DOMAINS:
            raise ValueError(f"email domain '{domain}' is not allowed")
        return email


class UserUpdateRequest(BaseModel):
    PASSWROD_FIELD: ClassVar[str] = "password"
    password: SecretStr | None = Field(default=None, min_length=PASSWORD_MIN_LENGTH)


class UserResponse(ResponseBase):
    user_id: int
    email: EmailStr


class TokenPayload(BaseModel):
    sub: str
    token_type: str
    exp: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str
