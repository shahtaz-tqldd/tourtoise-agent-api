from uuid import UUID
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from auth.db.crud import UserRepository
from auth.helpers.password import verify_password, hash_password
from auth.helpers.jwt import create_tokens, decode_jwt

from auth.schema import (
    UserPrivateResponseSchema
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db) 
        

    async def login(self, credentials: dict) -> dict:
        """Authenticate user and return their tokens"""
        
        user = await self.user_repo.get_user(user_email=credentials["email"])

        if not user:
            raise ValueError("This email is not registered!")

        if not verify_password(credentials["password"], user.hashed_password):
            raise ValueError("Your password is incorrect!")

        return create_tokens(str(user.user_id))

    
    async def register(self, user_info: dict) -> dict:
        """Register a new user and return their tokens"""

        user = await self.user_repo.get_user(user_email=user_info["email"])

        if user:
            raise ValueError("User with this email address already exists!")

        password = user_info.pop("password")
        user_info["hashed_password"] = hash_password(password)
        user = await self.user_repo.create_user(user_info)

        if not user:
            raise ValueError("User registration failed")

        return create_tokens(str(user.user_id))

    
    async def refresh(self, payload, refresh_token_cookie: Optional[str]) -> dict:
        """Refresh and return new tokens for the user"""
        # Prefer body token, fallback to cookie
        refresh_token = payload["refresh_token"] or refresh_token_cookie

        if not refresh_token:
            raise ValueError("Refresh token is required")

        decoded = decode_jwt(refresh_token)

        if not decoded or decoded.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = decoded["user_id"]
        return create_tokens(str(user_id))


    async def get_user(self, user_id: str) -> UserPrivateResponseSchema:
        """Get user information by user ID"""
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        
        if not user:
            raise ValueError("User not found")
        
        user_schema = UserPrivateResponseSchema.model_validate(user)
        
        return user_schema


    async def update_user(self, user_id: UUID, updates: dict) -> UserPrivateResponseSchema:
        """Update user information"""
        user = await self.user_repo.update_user(user_id=user_id, updates=updates)

        if not user:
            raise ValueError("User not found or update failed")

        user_schema = UserPrivateResponseSchema.model_validate(user)

        return user_schema
    

class AdminUserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db) 

    async def user_list(self, page, page_size, search_str):
        """Get user information by email"""
        return await self.user_repo.get_list(
            page=page, 
            page_size=page_size, 
            search_str=search_str
        )
        
        