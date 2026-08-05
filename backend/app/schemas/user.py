from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

from app.core.constants import (
    ALLOWED_EMAIL_DOMAINS,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)
from app.schemas.base import ResponseBase


class UserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: SecretStr = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_domain(cls, email: str) -> str:
        domain = email.split("@")[-1].lower()

        if domain not in ALLOWED_EMAIL_DOMAINS:
            raise ValueError(
                f"email domain '{domain}' is not allowed"
            )

        return email


class UserUpdateRequest(BaseModel):
    PASSWORD_FIELD: ClassVar[str] = "password"

    password: SecretStr | None = Field(
        default=None,
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )


class UserResponse(ResponseBase):
    user_id: int
    email: EmailStr


class TokenPayload(BaseModel):
    sub: str
    token_type: str = Field(alias="type")
    exp: datetime

    model_config = ConfigDict(
        populate_by_name=True
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str