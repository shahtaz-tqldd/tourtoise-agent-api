from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict, UUID4

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None

    # Localization
    language: Optional[str] = None
    timezone: Optional[str] = None

    # Full travel preferences
    travel_style: Optional[List[str]] = None
    budget_level: Optional[str] = None
    prefered_group: Optional[List[str]] = None
    food_preferences: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    # Location sharing status
    location_sharing_enabled: bool = False
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: UUID
    first_name: str
    last_name: Optional[str]
    email: str
    hashed_password: str
    is_active: bool


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    first_name: str
    last_name: Optional[str]
    email: str


class AccountType(str, Enum):
    REGULAR = "regular"
    ADMIN = "admin"
    STAFF = "staff"

class UserPublicResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID4
    first_name: str
    last_name: Optional[str] = None
    profile_image_url: Optional[str] = None
    
    # Optional public preferences
    travel_style: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    
    # Live location only if sharing is enabled
    location_sharing_enabled: bool = False
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    last_active_at: Optional[datetime] = None
    
    created_at: datetime


# Authenticated user response
class UserPrivateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID4
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    profile_image_url: Optional[str] = None

    # Localization
    language: str = "en"
    timezone: str = "UTC"

    # Full travel preferences
    travel_style: Optional[List[str]] = None
    budget_level: Optional[str] = None
    prefered_group: Optional[List[str]] = None
    food_preferences: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    # Location sharing status
    location_sharing_enabled: bool = False
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    last_active_at: Optional[datetime] = None

    # Account status
    email_verified: bool = False

    # Timestamps
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None


class UserBasicPrivateDetailsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    profile_image_url: Optional[str] = None

    # Location sharing status
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    last_active_at: Optional[datetime] = None

    
    # Timestamps
    created_at: datetime
    last_login_at: Optional[datetime] = None
