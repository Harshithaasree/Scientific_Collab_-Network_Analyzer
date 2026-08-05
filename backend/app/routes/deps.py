from typing import Annotated

from app.core import Config, get_config, get_db
from app.models import User
from app.schemas import TokenPayload
from app.services import AuthService, TokenService, UserService

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)

config: type[Config] = get_config()


# --------------------------------------------------
# Type aliases
# --------------------------------------------------

DBSession = Annotated[
    AsyncSession,
    Depends(get_db),
]

Token = Annotated[
    str,
    Depends(oauth2_scheme),
]


# --------------------------------------------------
# Dependency providers
# --------------------------------------------------

def get_user_service(
    session: DBSession,
) -> UserService:
    return UserService(session)


def get_token_service() -> TokenService:
    return TokenService(config)


def get_auth_service() -> AuthService:
    return AuthService(
        get_token_service()
    )


# --------------------------------------------------
# Auth guard
# --------------------------------------------------

async def get_current_user(
    token: Token,
    session: DBSession,
) -> User:

    token_service: TokenService = get_token_service()

    payload: TokenPayload = token_service.decode_token(token)

    if not payload.sub:
        raise HTTPException(
            status_code=401,
            detail="invalid token payload",
        )

    user: User | None = await UserService(
        session
    ).get_user_by_email(payload.sub)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="user not found",
        )

    return user


# --------------------------------------------------
# Annotated shortcuts for routes
# --------------------------------------------------

AuthServiceDeps = Annotated[
    AuthService,
    Depends(get_auth_service),
]

UserServiceDeps = Annotated[
    UserService,
    Depends(get_user_service),
]

CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]

