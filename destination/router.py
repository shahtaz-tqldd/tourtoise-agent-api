from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Cookie, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.schema import (
    BaseResponse, 
    DataResponse, 
    ListResponse
)
from app.utils.print_log import print_log
from destination.services import DestinationService

from destination.schema import (
    DestinationCreateRequest,
    AccommodationTypeRequest
)

from app.db.session import get_async_session
from auth.helpers.dependencies import get_current_user

router = APIRouter()

async def get_destination_service(
    db: AsyncSession = Depends(get_async_session),
) -> DestinationService:
    return DestinationService(db)


@router.get("", response_model=ListResponse)
async def list_destinations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search_query: Optional[str] = Query(None),
    service: DestinationService = Depends(get_destination_service),
    user_id: UUID = Depends(get_current_user)
):
    try:
        destination_list, total_count = await service.get_all_destinations(
            page,
            page_size,
            search_query,
        )
        return ListResponse(
            success=True,
            data=destination_list,
            page=page,
            page_size=page_size,
            total=total_count,
            message="Destination list fetched successfully.",
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create", response_model=DataResponse)
async def create_new_destination(
    destination_payload: DestinationCreateRequest = Body(...),
    service = Depends(get_destination_service),
    # user_id: UUID = Depends(get_current_user)
):
    try:
        destination_details = await service.create_destination(destination_payload.model_dump())
        return DataResponse(
            success=True,
            data=destination_details,
            message="A new destination created successfully!",
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# AccommodationTypeService
from destination.services.accommodation import AccommodationTypeService

async def get_accommodation_type_service(
    db: AsyncSession = Depends(get_async_session),
) -> AccommodationTypeService:
    return AccommodationTypeService(db)

@router.post("/accommodation-type/create", response_model=DataResponse)
async def create_accommodation_type(
    accommodation_payload: AccommodationTypeRequest = Body(...),
    service: AccommodationTypeService = Depends(get_accommodation_type_service),
):
    try:
        accommodation_type_details = await service.create_accommodation_type(accommodation_payload.model_dump)
        return DataResponse(
            success=True,
            data=accommodation_type_details,
            message="A new accommodation type created successfully!",
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/accommodation-type/list", response_model=DataResponse)
async def list_accommodation_types(
    service: AccommodationTypeService = Depends(get_accommodation_type_service),
):
    try:
        accommodation_type_list = await service.accommodation_type_list()

        return DataResponse(
            success=True,
            data=accommodation_type_list,
            message="Accommodation type list fetched successfully.",
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))