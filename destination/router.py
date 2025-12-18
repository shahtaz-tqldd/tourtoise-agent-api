from uuid import UUID
from typing import Optional
from app.utils.print_log import print_log
from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.schema import (
    BaseResponse, 
    DataResponse, 
    ListResponse
)
from destination.services import (
    DestinationService, 
    TransportTypeService, 
    AccommodationTypeService,
    ActivityTypeService,
)

from destination.schema import (
    DestinationCreateRequest,
    AccommodationTypeRequest,
    TransportTypeRequest,
    ActivityTypeRequest,
)

from app.db.session import get_async_session
from auth.helpers.dependencies import get_current_user

router = APIRouter()

# destination routes

async def get_destination_service(
    db: AsyncSession = Depends(get_async_session),
) -> DestinationService:
    return DestinationService(db)


@router.get("/list", response_model=ListResponse)
async def list_destinations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search_query: Optional[str] = Query(None),
    service: DestinationService = Depends(get_destination_service),
    # user_id: UUID = Depends(get_current_user)
):
    destination_list, total_count = await service.destination_list(
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


@router.post("/create", response_model=DataResponse)
async def create_new_destination(
    destination_payload: DestinationCreateRequest = Body(...),
    service: DestinationService = Depends(get_destination_service),
    # user_id: UUID = Depends(get_current_user)
):

    destination_details = await service.create_destination(destination_payload.model_dump())
    
    return DataResponse(
        success=True,
        data=destination_details,
        message="A new destination created successfully!",
    )



# accommodations routes

async def get_accommodation_type_service(
    db: AsyncSession = Depends(get_async_session),
) -> AccommodationTypeService:
    return AccommodationTypeService(db)

@router.post("/accommodation-type/create", response_model=DataResponse)
async def create_accommodation_type(
    accommodation_payload: AccommodationTypeRequest = Body(...),
    service: AccommodationTypeService = Depends(get_accommodation_type_service),
):
    accommodation_type_details = await service.create_accommodation_type(accommodation_payload.model_dump())
    return DataResponse(
        success=True,
        data=accommodation_type_details,
        message="A new accommodation type created successfully!",
    )


@router.get("/accommodation-type/list", response_model=DataResponse)
async def list_accommodation_types(
    service: AccommodationTypeService = Depends(get_accommodation_type_service),
):
    accommodation_type_list = await service.accommodation_type_list()

    return DataResponse(
        success=True,
        data=accommodation_type_list,
        message="Accommodation type list fetched successfully.",
    )



# transportation routes

async def get_transport_type_service(
    db: AsyncSession = Depends(get_async_session),
) -> TransportTypeService:
    return TransportTypeService(db)

@router.post("/transport-type/create", response_model=DataResponse)
async def create_transport_type(
    transport_payload: TransportTypeRequest = Body(...),
    service: TransportTypeService = Depends(get_transport_type_service),
):
    transport_type_details = await service.create_transport_type(transport_payload.model_dump())
    return DataResponse(
        success=True,
        data=transport_type_details,
        message="A new transport type created successfully!",
    )


@router.get("/transport-type/list", response_model=DataResponse)
async def list_transport_types(
    service: TransportTypeService = Depends(get_transport_type_service),
):
    transport_type_list = await service.transport_type_list()

    return DataResponse(
        success=True,
        data=transport_type_list,
        message="Transport type list fetched successfully.",
    )

   
# activity routes

async def get_activity_type_service(
    db: AsyncSession = Depends(get_async_session),
) -> ActivityTypeService:
    return ActivityTypeService(db)

@router.post("/activity-type/create", response_model=DataResponse)
async def create_activity_type(
    activity_payload: ActivityTypeRequest = Body(...),
    service: ActivityTypeService = Depends(get_activity_type_service),
):
    activity_type_details = await service.create_activity_type(activity_payload.model_dump())
    return DataResponse(
        success=True,
        data=activity_type_details,
        message="A new activity type created successfully!",
    )


@router.get("/activity-type/list", response_model=DataResponse)
async def list_activity_types(
    service: ActivityTypeService = Depends(get_activity_type_service),
):
    activity_type_list = await service.activity_type_list()

    return DataResponse(
        success=True,
        data=activity_type_list,
        message="Activity type list fetched successfully.",
    )

   