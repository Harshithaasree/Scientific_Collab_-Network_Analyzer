import logging

from core.constants import TokenType
from fastapi import HTTPException
from models import RevokedToken, User
from schemas import TokenPayload, TokenResponse, UserRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .token import TokenService
from .user import UserService

logger: logging.Logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service: TokenService = token_service

    async def login(
        self, credentials: UserRequest, user_service: UserService
    ) -> TokenResponse:
        logger.info("login attemp: %s", credentials.email)
        user: User | None = await user_service.get_user_by_email(credentials.email)
        if not user or not user.check_password(credentials.password):
            logger.warning("login failed, invalid credentials: %s", credentials.email)
            raise HTTPException(status_code=401, detail="invalid credentials")

        logger.info("login successful: %s", credentials.email)
        return TokenResponse(
            access_token=self.token_service.create_access_token(user.email),
            refresh_token=self.token_service.create_refresh_token(user.email),
            token_type=TokenType.BEARER,
        )

    def login_registered_user(self, user: User) -> TokenResponse:
        return TokenResponse(
            access_token=self.token_service.create_access_token(user.email),
            refresh_token=self.token_service.create_refresh_token(user.email),
            token_type=TokenType.BEARER,
        )

    async def logout(self, refresh_token: str, session: AsyncSession) -> None:
        blacklisted = RevokedToken(token=refresh_token)
        session.add(blacklisted)
        await session.commit()

    async def is_revoked(self, refresh_token: str, session: AsyncSession) -> bool:
        result: RevokedToken | None = await session.scalar(
            select(RevokedToken).where(RevokedToken.token == refresh_token)
        )
        return result is not None

    async def refresh(
        self, refresh_token: str, user_service: UserService, session: AsyncSession
    ) -> TokenResponse:
        if await self.is_revoked(refresh_token, session):
            raise HTTPException(status_code=401, detail="token has be revoked")

        payload: TokenPayload = self.token_service.decode_token(refresh_token)
        if payload.token_type != TokenType.REFRESH:
            raise HTTPException(status_code=401, detail="invalid token type")
        if not payload.sub:
            raise HTTPException(status_code=401, detail="invalid token payload")

        user: User | None = await user_service.get_user_by_email(payload.sub)
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        return TokenResponse(
            access_token=self.token_service.create_access_token(payload.sub),
            token_type=TokenType.BEARER,
        )
