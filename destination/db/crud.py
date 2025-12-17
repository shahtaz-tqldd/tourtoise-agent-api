from typing import List, Tuple
from destination.schema import (
  DestinationDetails, 
  ShortDestinationDetails,
  AccommodationTypeDetails,
  AccommodationTypeRequest
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from destination.db.models import AccommodationTypeRef

class DestinationCRUD:
  def __init__(self, db: AsyncSession):
    self.db = db
  
  async def create_destination(self, destination_data: dict) -> DestinationDetails:
    new_destination = DestinationDetails(**destination_data)
    self.db.add(new_destination)
    self.db.commit()
    self.db.refresh(new_destination)
    return new_destination
      
  async def get_all_destinations(
    self, 
    page: int = 1, 
    page_size: int = 10, 
    search_query: str = None
  ) -> Tuple[List[ShortDestinationDetails], int]:
    query = self.db.query(ShortDestinationDetails)

    if search_query:
      query = query.filter(ShortDestinationDetails.name.ilike(f"%{search_query}%"))

    total_count = await query.count()
    destinations = await query.offset((page - 1) * page_size).limit(page_size).all()

    return destinations, total_count
      

class AccommodationCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_accommodation_type(self, accommodation_data: dict):
        new_accommodation = AccommodationTypeRef(**accommodation_data)
        self.db.add(new_accommodation)
        await self.db.commit()  # ✅ Added await
        await self.db.refresh(new_accommodation)  # ✅ Added await
        return new_accommodation
    
    async def accommodation_type_list(self) -> List[AccommodationTypeDetails]:
        stmt = select(AccommodationTypeRef)
        result = await self.db.execute(stmt)
        rows = result.scalars().all()

        return [AccommodationTypeDetails.model_validate(row) for row in rows]