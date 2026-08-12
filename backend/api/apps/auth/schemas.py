from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class UserRegister(UserBase):

    password: str = Field(..., min_length=8, max_length=255)


class UserLogin(BaseModel):

    email: EmailStr
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):

    id: str
    is_active: bool
    created_at: datetime
    meliponary_name: Optional[str] = "Meu Meliponário"
    meliponary_location: Optional[str] = None
    inspection_frequency_days: Optional[int] = 14
    notify_health_alerts: Optional[bool] = True
    notify_email: Optional[bool] = True
    auth_provider: Optional[str] = "local"
    picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    meliponary_name: Optional[str] = Field(None, max_length=255)
    meliponary_location: Optional[str] = Field(None, max_length=255)
    inspection_frequency_days: Optional[int] = Field(None, ge=1, le=365)
    notify_health_alerts: Optional[bool] = None
    notify_email: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=255)
    confirm_password: str = Field(..., min_length=8, max_length=255)


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6)

    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
