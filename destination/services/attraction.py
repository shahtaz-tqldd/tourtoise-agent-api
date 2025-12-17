
from destination.db.crud import DestinationCRUD

class DestinationService:
  def __init__(self, db):
    self.db = db
    self.destination_crud = DestinationCRUD(db)

  async def create_destination(self, destination_data: dict):
    # 1. create destination in Database
    created_destination = await self.destination_crud.create_destination(destination_data)

    # 2. bring vector resources

    # 3. Update data to the vector DB

    return created_destination