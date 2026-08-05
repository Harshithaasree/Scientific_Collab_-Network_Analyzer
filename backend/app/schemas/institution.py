from datetime import datetime

from pydantic import Field

from .base import ResponseBase
from .common import CreateBase, UpdateBase


class InstitutionRequest(CreateBase):
    name: str = Field(min_length=1, max_length=255)
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=255)


class InstitutionUpdateRequest(UpdateBase):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=255)


class InstitutionResponse(ResponseBase):
    institution_id: int
    name: str
    country: str | None
    city: str | None
    website: str | None
    created_at: datetime