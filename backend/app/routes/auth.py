from fastapi import APIRouter
from models import User
from schemas import RefreshRequest, TokenResponse, UserRequest

from .deps import AuthServiceDeps, DBSession, UserServiceDeps

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", status_code=201)
async def register(
    credentials: UserRequest,
    user_service: UserServiceDeps,
    auth_servie: AuthServiceDeps,
) -> TokenResponse:
    user: User = await user_service.register(credentials)
    return auth_servie.login_registered_user(user)


@auth_router.post("/login")
async def login(
    credentials: UserRequest,
    user_service: UserServiceDeps,
    auth_service: AuthServiceDeps,
) -> TokenResponse:
    return await auth_service.login(credentials, user_service)


@auth_router.post("/logout", status_code=204)
async def logout(
    body: RefreshRequest, auth_service: AuthServiceDeps, session: DBSession
) -> None:
    return await auth_service.logout(body.refresh_token, session)


@auth_router.post("/refresh")
async def refresh_token(
    body: RefreshRequest,
    user_service: UserServiceDeps,
    auth_service: AuthServiceDeps,
    session: DBSession,
) -> TokenResponse:
    return await auth_service.refresh(body.refresh_token, user_service, session)
