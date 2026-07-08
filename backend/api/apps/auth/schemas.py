"""Auth schemas - Pydantic models for API requests/responses."""

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

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"
