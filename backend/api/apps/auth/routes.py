from datetime import timedelta

from fastapi import APIRouter, Depends, Request, Response
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.dependencies import get_current_user, get_db
from .models import User
from .schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    ForgotPasswordRequest,
    VerifyResetCodeRequest,
    ResetPasswordRequest,
)
from .services.service import AuthService
from .services.google_service import oauth

settings = get_settings()

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
        key="melitrack_session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60,  # 24 hours
    )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )


@router.get("/google")
async def login_google(request: Request):
    redirect_to = request.query_params.get("redirect_to")
    if redirect_to:
        request.session["auth_redirect_to"] = redirect_to

    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]

    user = await AuthService.authenticate_google(
        db,
        user_info,
    )

    jwt = AuthService.create_token(user.id)
    redirect_to = request.session.pop("auth_redirect_to", None)

    response.set_cookie(
        key="melitrack_session",
        value=jwt,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=24 * 60 * 60,
        path="/",
    )

    if redirect_to:
        redirect_url = redirect_to
        if "?" in redirect_url:
            redirect_url = f"{redirect_url}&auth=google"
        else:
            redirect_url = f"{redirect_url}?auth=google"

        redirect_response = RedirectResponse(redirect_url)
        response.set_cookie(
            key="melitrack_session",
            value=jwt,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=24 * 60 * 60,
            path="/",
        )

    if redirect_to:
        redirect_url = redirect_to
        if "?" in redirect_url:
            redirect_url = f"{redirect_url}&auth=google"
        else:
            redirect_url = f"{redirect_url}?auth=google"

        redirect_response = RedirectResponse(redirect_url)
        redirect_response.set_cookie(
            key="melitrack_session",
            value=jwt,
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=24 * 60 * 60,
            path="/",
        )
        return redirect_response

    return {
        "access_token": jwt,
    }


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie("melitrack_session")
    return {"message": "Logged out successfully"}


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    await AuthService.forgot_password(db, request.email)

    return {"message": "If the email exists, a recovery code has been sent."}


@router.post("/verify-reset-code")
async def verify_reset_code(
    request: VerifyResetCodeRequest,
    db: AsyncSession = Depends(get_db),
):
    await AuthService.verify_reset_code(
        db,
        request.email,
        request.code,
    )

    return {"valid": True}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    await AuthService.reset_password(
        db,
        request.email,
        request.code,
        request.new_password,
        request.confirm_password,
    )

    return {"message": "Password updated successfully"}
