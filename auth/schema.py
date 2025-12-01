from uuid import UUID

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.base.schema import BaseResponse

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

class UserResponse(BaseResponse):
    data: UserResponseSchema