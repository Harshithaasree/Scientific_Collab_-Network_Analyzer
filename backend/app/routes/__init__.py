from fastapi import APIRouter

from .auth import auth_router

# from .citation import citation_router
# from .collaboration import collaboration_router
# from .conference import conference_router
# from .dashboard import dashboard_router
# from .project import project_router
# from .publication import publication_router
# from .report import report_router
# from .researcher import researcher_router
from .user import user_router

router = APIRouter()
router.include_router(auth_router)
# router.include_router(citation_router)
# router.include_router(collaboration_router)
# router.include_router(conference_router)
# router.include_router(dashboard_router)
# router.include_router(project_router)
# router.include_router(publication_router)
# router.include_router(report_router)
# router.include_router(researcher_router)
router.include_router(user_router)
