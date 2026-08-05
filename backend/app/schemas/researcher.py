from datetime import datetime

from pydantic import Field

from .base import ResponseBase
from .common import CreateBase, UpdateBase


class ResearcherRequest(CreateBase):
    user_id: int
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    institution_id: int | None = None
    affiliation: str | None = Field(default=None, max_length=255)
    research_area: str | None = Field(default=None, max_length=255)
    bio: str | None = None


class ResearcherUpdateRequest(UpdateBase):
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    institution_id: int | None = None
    affiliation: str | None = Field(default=None, max_length=255)
    research_area: str | None = Field(default=None, max_length=255)
    bio: str | None = None


class ResearcherResponse(ResponseBase):
    researcher_id: int
    user_id: int
    institution_id: int | None
    first_name: str
    last_name: str
    affiliation: str | None
    research_area: str | None
    bio: str | None
    created_at: datetime