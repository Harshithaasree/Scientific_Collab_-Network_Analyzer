from .base import ResponseBase
from .citation import CitationRequest, CitationResponse
from .collaboration import (
    CollaborationRequest,
    CollaborationResponse,
    CollaborationUpdateRequest,
)
from .conference import (
    ConferenceRequest,
    ConferenceResponse,
    ConferenceUpdateRequest,
)
from .institution import (
    InstitutionRequest,
    InstitutionResponse,
    InstitutionUpdateRequest,
)
from .project import (
    ProjectRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from .publication import (
    PublicationRequest,
    PublicationResponse,
    PublicationUpdateRequest,
)
from .researcher import (
    ResearcherRequest,
    ResearcherResponse,
    ResearcherUpdateRequest,
)
from .user import (
    RefreshRequest,
    TokenPayload,
    TokenResponse,
    UserRequest,
    UserResponse,
    UserUpdateRequest,
)

__all__: list[str] = [
    "CitationRequest",
    "CitationResponse",
    "CollaborationRequest",
    "CollaborationResponse",
    "CollaborationUpdateRequest",
    "ConferenceRequest",
    "ConferenceResponse",
    "ConferenceUpdateRequest",
    "InstitutionRequest",
    "InstitutionResponse",
    "InstitutionUpdateRequest",
    "ProjectRequest",
    "ProjectResponse",
    "ProjectUpdateRequest",
    "PublicationRequest",
    "PublicationResponse",
    "PublicationUpdateRequest",
    "RefreshRequest",
    "ResearcherRequest",
    "ResearcherResponse",
    "ResearcherUpdateRequest",
    "ResponseBase",
    "TokenPayload",
    "TokenResponse",
    "UserRequest",
    "UserResponse",
    "UserUpdateRequest",
]