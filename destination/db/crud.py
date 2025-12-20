from uuid import UUID
from decimal import Decimal
from typing import List, Tuple, Optional, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from destination.schema import (
  DestinationDetails, 
  DestinationBasicDetails,
  AccommodationTypeDetails,
  TransportTypeDetails,
  ActivityTypeDetails,
  DestinationImageDetails
)


from destination.db.models import (
    Destination,
    AccommodationTypeRef,
    DestinationAccommodationType,
    Accommodation,
    TransportTypeRef,
    DestinationTransportOption,
    ActivityTypeRef,
    DestinationActivity,
    SignatureDish,
    Attraction,
    DietaryEnum,
    DestinationImage,
    AttractionImage,
)


class DestinationCRUD:
    def __init__(self, db: AsyncSession):
      self.db = db
  
    async def create(self, destination_data: dict) -> DestinationDetails:
        """
        Create a destination with all nested relationships
        """
        try:
            # Extract nested data
            accommodation_types_data = destination_data.pop("accommodation_types", [])
            accommodations_data = destination_data.pop("accommodations", [])
            transport_options_data = destination_data.pop("transport_options", [])
            activities_data = destination_data.pop("activities", [])
            signature_dishes_data = destination_data.pop("signature_dishes", [])
            attractions_data = destination_data.pop("attractions", [])

            # Convert string decimal fields to Decimal for main destination
            if destination_data.get("longitude"):
                destination_data["longitude"] = Decimal(str(destination_data["longitude"]))
            
            if destination_data.get("latitude"):
                destination_data["latitude"] = Decimal(str(destination_data["latitude"]))

            # Create the main destination
            new_destination = Destination(**destination_data)
            self.db.add(new_destination)
            await self.db.flush()

            # Create accommodation types
            accommodation_type_map = {}
            for acc_type_data in accommodation_types_data:
                accommodation_type = DestinationAccommodationType(
                    destination_id=new_destination.id,
                    type_ref_id=UUID(acc_type_data["accommodation_type_id"]),
                    price_range=acc_type_data["price_range"],
                    availability=acc_type_data.get("availability"),
                    description=acc_type_data.get("description"),
                )
                self.db.add(accommodation_type)
                await self.db.flush()
                
                accommodation_type_map[acc_type_data["accommodation_type_id"]] = accommodation_type.id

            # Create transport options
            for transport_data in transport_options_data:
                transport_option = DestinationTransportOption(
                    destination_id=new_destination.id,
                    transport_ref_id=UUID(transport_data["transport_type_id"]),
                    price_range=transport_data["price_range"],
                    availability=transport_data.get("availability"),
                    description=transport_data.get("description"),
                )
                self.db.add(transport_option)

            # Create activities
            for activity_data in activities_data:
                activity = DestinationActivity(
                    destination_id=new_destination.id,
                    activity_ref_id=UUID(activity_data["activity_type_id"]),
                    price_range=activity_data.get("price_range"),
                    duration=activity_data.get("duration"),
                    best_season=activity_data.get("best_season"),
                    booking_required=activity_data.get("booking_required", False),
                    is_popular=activity_data.get("is_popular", False),
                    description=activity_data.get("description"),
                )
                self.db.add(activity)

            # Create signature dishes
            for dish_data in signature_dishes_data:
                # Parse tags (can be comma-separated string or list)
                tags = dish_data.get("tags")
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(",")]
                
                # Parse dietary info (can be comma-separated string or list)
                dietary_info = dish_data.get("dietary_info")
                dietary_enums = []
                if dietary_info:
                    if isinstance(dietary_info, str):
                        dietary_list = [d.strip().lower() for d in dietary_info.split(",")]
                    else:
                        dietary_list = [d.lower() for d in dietary_info]
                    
                    # Map to enum values
                    dietary_map = {
                        "vegetarian": DietaryEnum.VEG,
                        "non-vegetarian": DietaryEnum.NON_VEGAN,
                        "halal": DietaryEnum.HALAL,
                        "other": DietaryEnum.OTHER,
                    }
                    dietary_enums = [dietary_map.get(d, DietaryEnum.OTHER) for d in dietary_list]

                signature_dish = SignatureDish(
                    destination_id=new_destination.id,
                    name=dish_data["name"],
                    tags=tags,
                    dietary_info=dietary_enums if dietary_enums else None,
                    price_range=dish_data.get("price_range"),
                    is_recommended=dish_data.get("is_recommended", False),
                    local_notes=dish_data.get("local_notes"),
                )
                self.db.add(signature_dish)

            # Create accommodations
            for acc_data in accommodations_data:
                type_ref_id = acc_data.get("accommodation_type_id")
                junction_table_id = accommodation_type_map.get(type_ref_id) if type_ref_id else None
                
                accommodation = Accommodation(
                    destination_id=new_destination.id,
                    accommodation_type_id=junction_table_id,
                    name=acc_data["name"],
                    price_range=acc_data["price_range"],
                    rating=Decimal(str(acc_data["rating"])) if acc_data.get("rating") else None,
                    distance=acc_data.get("distance"),
                    region=acc_data["region"],
                    longitude=Decimal(str(acc_data["longitude"])) if acc_data.get("longitude") else None,
                    latitude=Decimal(str(acc_data["latitude"])) if acc_data.get("latitude") else None,
                    phone=acc_data.get("phone"),
                    email=acc_data.get("email"),
                    website=acc_data.get("website"),
                )
                self.db.add(accommodation)

            # Create attractions
            for attr_data in attractions_data:
                attraction = Attraction(
                    destination_id=new_destination.id,
                    name=attr_data["name"],
                    description=attr_data.get("description"),
                    tag=attr_data.get("tag"),
                    entry_fee=attr_data.get("entry_fee"),
                    opening_hours=attr_data.get("opening_hours"),
                    best_time_to_visit=attr_data.get("best_time_to_visit"),
                    available_transports=attr_data.get("available_transports", []),
                    is_recommended=attr_data.get("is_recommended", False),
                    region=attr_data["region"],
                    longitude=Decimal(str(attr_data["longitude"])) if attr_data.get("longitude") else None,
                    latitude=Decimal(str(attr_data["latitude"])) if attr_data.get("latitude") else None,
                )
                self.db.add(attraction)

            # Commit all changes
            await self.db.commit()
            
            stmt = (
                select(Destination)
                .options(selectinload(Destination.attractions))
                .where(Destination.id == new_destination.id)
            )

            result = await self.db.execute(stmt)
            destination = result.scalar_one()

            return DestinationDetails.model_validate(destination)

        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error creating destination: {str(e)}")

    async def add_destination_images(self, image_data: List[Dict[str, Any]]) -> list[DestinationImageDetails]:
        if not image_data:
            return []

        created_images = []

        for img in image_data:
            dest_img = DestinationImage(
                destination_id=img["destination_id"],
                image_url=img["image_url"],
                public_id=img["public_id"],
                alt_text=img.get("alt_text"),
            )
            self.db.add(dest_img)
            created_images.append(dest_img)

        await self.db.commit()

        for img in created_images:
            await self.db.refresh(img)

        return created_images

    async def add_attraction_images(self, image_data: List[Dict[str, Any]]) -> list[DestinationImageDetails]:
        if not image_data:
            return []

        created_images = []

        for img in image_data:
            attraction_img = AttractionImage(
                attraction_id=img["attraction_id"],
                image_url=img["image_url"],
                public_id=img["public_id"],
                alt_text=img.get("alt_text"),
            )
            self.db.add(attraction_img)
            created_images.append(attraction_img)

        await self.db.commit()

        for img in created_images:
            await self.db.refresh(img)

        return created_images
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search_query: str | None = None,
    ) -> Tuple[List[DestinationBasicDetails], int]:

        stmt = (
            select(Destination)
            .options(selectinload(Destination.images))
        )

        if search_query:
            stmt = stmt.where(Destination.name.ilike(f"%{search_query}%"))

        # Total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db.scalar(count_stmt)

        # Pagination
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)
        destinations = result.scalars().all()

        return (
            [DestinationBasicDetails.model_validate(d) for d in destinations],
            total
        )


    async def delete(self, destination_id) -> None:
        stmt = select(Destination).where(Destination.id == destination_id)
        result = await self.db.execute(stmt)
        destination = result.scalar_one_or_none()

        if not destination:
            raise ValueError("Destination not found")

        await self.db.delete(destination)
        await self.db.commit()

class AccommodationCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_accommodation_type(self, accommodation_data: dict) -> AccommodationTypeDetails:
        new_accommodation = AccommodationTypeRef(**accommodation_data)
        self.db.add(new_accommodation)
        await self.db.commit()
        await self.db.refresh(new_accommodation)
        return AccommodationTypeDetails.model_validate(new_accommodation)
    
    async def accommodation_type_list(self) -> List[AccommodationTypeDetails]:
        stmt = select(AccommodationTypeRef)
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        return [AccommodationTypeDetails.model_validate(row) for row in rows]
    
    async def get_accommodation_type_by_id(self, type_id: UUID) -> Optional[AccommodationTypeRef]:
        """Get accommodation type reference by ID"""
        result = await self.db.execute(
            select(AccommodationTypeRef).where(AccommodationTypeRef.id == type_id)
        )
        return result.scalar_one_or_none()


class TransportCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transport_type(self, transport_data: dict) -> TransportTypeDetails:
        new_transport = TransportTypeRef(**transport_data)
        self.db.add(new_transport)
        await self.db.commit()
        await self.db.refresh(new_transport)
        return TransportTypeDetails.model_validate(new_transport)

    async def transport_type_list(self) -> List[TransportTypeDetails]:
        stmt = select(TransportTypeRef)
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        return [TransportTypeDetails.model_validate(row) for row in rows]

    async def get_transport_type_by_id(self, type_id: UUID) -> Optional[TransportTypeRef]:
        """Get transport type reference by ID"""
        result = await self.db.execute(
            select(TransportTypeRef).where(TransportTypeRef.id == type_id)
        )
        return result.scalar_one_or_none()


class ActivityCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_activity_type(self, activity_data: dict) -> ActivityTypeDetails:
        new_activity = ActivityTypeRef(**activity_data)
        self.db.add(new_activity)
        await self.db.commit()
        await self.db.refresh(new_activity)
        return ActivityTypeDetails.model_validate(new_activity)

    async def activity_type_list(self) -> List[ActivityTypeDetails]:
        stmt = select(ActivityTypeRef)
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        return [ActivityTypeDetails.model_validate(row) for row in rows]
    

    async def get_activity_type_by_id(self, type_id: UUID) -> Optional[ActivityTypeRef]:
        """Get activity type reference by ID"""
        result = await self.db.execute(
            select(ActivityTypeRef).where(ActivityTypeRef.id == type_id)
        )
        return result.scalar_one_or_none()