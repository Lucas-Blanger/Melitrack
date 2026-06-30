from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db
from .schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from .service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserRegister, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = await AuthService.register_user(db, user_data)
    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin, response: Response, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    # Authenticate user
    user = await AuthService.authenticate_user(db, credentials)

    # Create token
    access_token_expires = timedelta(hours=24)
    token = AuthService.create_token(user.id, access_token_expires)

    # Set HttpOnly cookie
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60,  # 24 hours
    )

    return TokenResponse(access_token=token)


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie("session")
    return {"message": "Logged out successfully"}
