import re

from core import PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, USERNAME_MAX_LENGTH
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .base import ResponseBase


class UserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH
    )
    user_name: str | None = Field(default=None, max_length=USERNAME_MAX_LENGTH)

    @field_validator("user_name")
    @classmethod
    def validate_name(cls, name: str | None) -> None | str:
        if name is not None and not re.match(r"^[A-Za-z\s\-']+$", name):
            raise ValueError("invalid user name")
        return name


class UserResponse(ResponseBase):
    user_id: int
    email: EmailStr
