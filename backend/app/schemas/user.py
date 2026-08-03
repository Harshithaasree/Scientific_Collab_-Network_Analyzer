import re
from datetime import datetime
from typing import ClassVar

from core.constants import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
)
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator

from .base import ResponseBase


class UserBase(BaseModel):
    user_name: str | None = Field(default=None, max_length=USERNAME_MAX_LENGTH)

    @field_validator("user_name")
    @classmethod
    def validate_name(cls, name: str | None) -> None | str:
        if name is not None and not re.match(r"^[A-Za-z\s\-']+$", name):
            raise ValueError("invalid user name")
        return name


class UserRequest(UserBase):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: SecretStr = Field(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )


class UserUpdateRequest(UserBase):
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
