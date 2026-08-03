from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from core import Config
from core.constants import TokenFields, TokenType
from fastapi import HTTPException
from models import User
from schemas import TokenPayload, TokenResponse, UserRequest

from .user import UserService


class TokenService:
    def __init__(self, config: type[Config]) -> None:
        self.config = config

    def create_access_token(self, email: str) -> str:
        payload: dict[str, str | datetime] = {
            TokenFields.SUBJECT: email,
            TokenFields.TYPE: TokenType.ACCESS,
            TokenFields.EXPIRY: datetime.now(UTC)
            + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(
            payload=payload,
            key=self.config.JWT_KEY.get_secret_value(),
            algorithm=self.config.ALGORITHM,
        )

    def create_refresh_token(self, email: str) -> str:
        payload: dict[str, str | datetime] = {
            TokenFields.SUBJECT: email,
            TokenFields.TYPE: TokenType.REFRESH,
            TokenFields.EXPIRY: datetime.now(UTC)
            + timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        return jwt.encode(
            payload=payload,
            key=self.config.JWT_KEY.get_secret_value(),
            algorithm=self.config.ALGORITHM,
        )

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload: dict[str, Any] = jwt.decode(
                jwt=token,
                key=self.config.JWT_KEY.get_secret_value(),
                algorithms=[self.config.ALGORITHM],
            )
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="invalid token")


class AuthService:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service: TokenService = token_service

    async def login(
        self, credentials: UserRequest, user_service: UserService
    ) -> TokenResponse:
        user: User | None = await user_service.get_user_by_email(credentials.email)
        if not user or not user.check_password(credentials.password):
            raise HTTPException(status_code=401, detail="invalid credentials")
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

    async def refresh(
        self, refresh_token: str, user_service: UserService
    ) -> TokenResponse:
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
