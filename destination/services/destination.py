from uuid import UUID
from app.utils.print_log import print_log
from destination.db.crud import DestinationCRUD, AccommodationCRUD, TransportCRUD, ActivityCRUD
from typing import Optional

class DestinationService:
  def __init__(self, db):
    self.db = db
    self.destination_crud = DestinationCRUD(db)
    self.accommodation_crud = AccommodationCRUD(db)
    self.transport_crud = TransportCRUD(db)
    self.activity_crud = ActivityCRUD(db)


  async def _validate_reference_ids(self, destination_data: dict):
    """
    Validate that all referenced accommodation, transport, and activity types exist
    """
    # Validate accommodation types
    for acc_type in destination_data.get("accommodation_types", []):
      type_id = UUID(acc_type["accommodation_type_id"])
      exists = await self.accommodation_crud.get_accommodation_type_by_id(type_id)
      if not exists:
        raise ValueError(f"Accommodation type with ID {type_id} does not exist")

    # Validate transport types
    for transport in destination_data.get("transport_options", []):
      type_id = UUID(transport["transport_type_id"])
      exists = await self.transport_crud.get_transport_type_by_id(type_id)
      if not exists:
        raise ValueError(f"Transport type with ID {type_id} does not exist")

    # Validate activity types
    for activity in destination_data.get("activities", []):
      type_id = UUID(activity["activity_type_id"])
      exists = await self.activity_crud.get_activity_type_by_id(type_id)
      if not exists:
        raise ValueError(f"Activity type with ID {type_id} does not exist")
            
  async def create_destination(self, destination_data: dict):
    # 1. create destination in Database
    
    try:
      # Validate that referenced types exist
      await self._validate_reference_ids(destination_data)
      
      
      new_destination = await self.destination_crud.create_destination(destination_data)
      
      return new_destination
        
    except Exception as e:
      raise Exception(f"Failed to create destination: {str(e)}")

    # 2. bring vector resources

    # 3. Update data to the vector DB

    return created_destination

  async def destination_list(
      self, 
      page: int, 
      page_size: int = 10, 
      search_query: Optional[str] = None
    ):
    
    destination_list, total_count = await self.destination_crud.get_list(
      page, 
      page_size, 
      search_query
    )
    return destination_list, total_count