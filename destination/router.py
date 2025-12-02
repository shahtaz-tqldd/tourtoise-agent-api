from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.schema import DataResponse

from app.db.session import get_async_session
from auth.helpers.dependencies import get_current_user

router = APIRouter()

@router.get("", response_model=DataResponse)
async def get_places(
    db: AsyncSession = Depends(get_async_session),
    user_id: UUID = Depends(get_current_user)
):
    try:
    
        
        return DataResponse(
            success=True,
            message="User fetched successfully",
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
