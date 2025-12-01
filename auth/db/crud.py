from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.db.models import User
from auth.schema import UserSchema

class UserRepository:
    @staticmethod
    async def get_user(db: AsyncSession, user_email: str) -> UserSchema | None:
        """Get user from user email"""
        stmt = select(User).where(User.email == user_email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> UserSchema | None:
        """Get user from user ID"""
        stmt = select(User).where(User.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict) -> UserSchema:
        """Create a new user"""
        new_user = User(**user_data)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    