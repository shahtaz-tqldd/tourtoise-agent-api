from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from auth.helpers.dependencies import get_current_user

from auth.services import AuthService
from auth.schema import (
    LoginRequest, 
    RegisterRequest,
    LoginResponse,
    RefreshRequest,
    UserResponse
)

from app.db.session import get_async_session

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(db)
    try:
        auth = await auth_service.login(payload.dict())
        return LoginResponse(**auth)
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register", response_model=LoginResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_async_session)):
    try:
        auth_service = AuthService(db)
        auth = await auth_service.register(payload.dict())
        return LoginResponse(**auth)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    payload: RefreshRequest = Body(...),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        auth_service = AuthService(db)
        new_token = await auth_service.refresh(payload.dict(), refresh_token_cookie)
        return LoginResponse(**new_token)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user")
async def get_user(
    db: AsyncSession = Depends(get_async_session),
    user_id: UUID = Depends(get_current_user)
):
    try:
    
        auth_service = AuthService(db)
        user = await auth_service.get_user(user_id)
        return UserResponse(
            success=True,
            message="User fetched successfully",
            data=user
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    