from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, Body, Cookie, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.schema import DataResponse, ListResponse

from auth.helpers.dependencies import get_current_user

from auth.services import AuthService, AdminUserService
from auth.schema import (
    LoginRequest, 
    RegisterRequest,
    RefreshRequest,
    UserUpdateRequest
)

from app.db.session import get_async_session

router = APIRouter()

def get_auth_service(
    db: AsyncSession = Depends(get_async_session),
) -> AuthService:
    return AuthService(db)

@router.post("/login", response_model=DataResponse)
async def login(
    payload: LoginRequest, 
    service: AuthService = Depends(get_auth_service)
):
    auth = await service.login(payload.model_dump())
    return DataResponse(
        success=True,
        message="Login successful",
        data=auth
    )



@router.post("/register", response_model=DataResponse)
async def register(
    payload: RegisterRequest, 
    service: AuthService = Depends(get_auth_service)
):    
    auth = await service.register(payload.model_dump())
    return DataResponse(
        success=True,
        message="Registration successful",
        data=auth
    )



@router.post("/refresh", response_model=DataResponse)
async def refresh(
    payload: RefreshRequest = Body(...),
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
    service: AuthService = Depends(get_auth_service)
):
    new_token = await service.refresh(payload.model_dump(), refresh_token_cookie)
    return DataResponse(
        success=True,
        message="Token refreshed successfully",
        data=new_token
    )


@router.get("/profile", response_model=DataResponse)
async def get_user(
    service: AuthService = Depends(get_auth_service),
    user_id: UUID = Depends(get_current_user)
):

    user = await service.get_user(user_id)
    return DataResponse(
        success=True,
        message="User fetched successfully",
        data=user
    )

@router.patch("/update-user")
async def update_user(
    payload: UserUpdateRequest = Body(...),
    service: AuthService = Depends(get_auth_service),
    user_id: UUID = Depends(get_current_user),
):
    user = await service.update_user(
        user_id = user_id, 
        updates = payload.model_dump(exclude_unset=True)
    )

    return DataResponse(
        success=True,
        message="User updated successfully!",
        data=user
    )

# admin services
def get_admin_user_service(
    db: AsyncSession = Depends(get_async_session),
) -> AdminUserService:
    return AdminUserService(db)

@router.get("/list", response_model=ListResponse)
async def get_user_list(
    page: int = Query(..., ge=1),
    page_size: int = Query(..., ge=1, le=1000),
    search_str: Optional[str] = None,
    service: AdminUserService = Depends(get_admin_user_service),
    # user_id: UUID = Depends(get_current_user)
):
    user_list, total_items = await service.user_list(
        page=page, 
        page_size=page_size, 
        search_str=search_str
    )
    return ListResponse(
        success=True,
        message="User list fetched successfully",
        data=user_list,
        page=page,
        page_size=page_size,
        total=total_items
    )

