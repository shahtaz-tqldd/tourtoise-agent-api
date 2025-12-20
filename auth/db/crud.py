from uuid import UUID
from typing import List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from auth.db.models import User
from auth.schema import UserSchema, UserBasicPrivateDetailsSchema

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db 

    async def get_list(
        self,
        page: int, 
        page_size: int, 
        search_str: Optional[str] = None
    ) -> Tuple[List[UserBasicPrivateDetailsSchema], int]:
        """Get a list of users with pagination and search"""
        stmt = select(User)
        if search_str:
            stmt = stmt.where(User.email.contains(search_str))
            
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(stmt)

        users = result.scalars().all()
        user_schemas = [
            UserBasicPrivateDetailsSchema.model_validate(user)
            for user in users
        ]

        count_stmt = select(func.count(User.user_id))
        if search_str:
            count_stmt = count_stmt.where(User.email.contains(search_str))

        total_items = (await self.db.execute(count_stmt)).scalar_one()

        return user_schemas, total_items

    
    async def get_user(self, user_email: str) -> UserSchema | None:
        """Get user from user email"""
        stmt = select(User).where(User.email == user_email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    
    async def get_user_by_id(self, user_id: str) -> UserSchema | None:
        """Get user from user ID"""
        stmt = select(User).where(User.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def create_user(self, user_data: dict) -> UserSchema:
        """Create a new user"""
        new_user = User(**user_data)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    

    async def update_user(self, user_id: UUID, updates: dict) -> UserSchema | None:
        """Update user information with user_id"""
        stmt = select(User).where(User.user_id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                print(f"Warning: Trying to set non-existent field: {key}")

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
