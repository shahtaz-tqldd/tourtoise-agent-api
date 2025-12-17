
from destination.db.crud import DestinationCRUD
from typing import Optional

class DestinationService:
  def __init__(self, db):
    self.db = db
    self.destination_crud = DestinationCRUD(db)

  async def create_destination(self, destination_data: dict):
    # 1. create destination in Database
    print("Creating destination: -----------------------------------------------")
    print(destination_data)
    print("-----------------------------------------------")

    return {}

    created_destination = await self.destination_crud.create_destination(
      destination_data
    )

    # 2. bring vector resources

    # 3. Update data to the vector DB

    return created_destination

  async def get_destination_list(
      self, 
      page: int, 
      page_size: int = 10, 
      search_query: Optional[str] = None
    ):
    
    destination_list, total_count = await self.destination_crud.get_all_destinations(
      page, 
      page_size, 
      search_query
    )
    return destination_list, total_count