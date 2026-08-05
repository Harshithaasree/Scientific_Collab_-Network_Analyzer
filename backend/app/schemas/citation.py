from datetime import datetime

from pydantic import Field, model_validator

from .base import ResponseBase
from .common import CreateBase


class CitationRequest(CreateBase):
    citing_publication_id: int
    cited_publication_id: int

    @model_validator(mode="after")
    def validate_different_publications(self):
        if (
            self.citing_publication_id
            == self.cited_publication_id
        ):
            raise ValueError(
                "A publication cannot cite itself"
            )

        return self


class CitationResponse(ResponseBase):
    citation_id: int
    citing_publication_id: int
    cited_publication_id: int
    created_at: datetime