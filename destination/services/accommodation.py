from destination.db.crud import AccommodationCRUD

class AccommodationTypeService:
  def __init__(self, db):
    self.db = db
    self.accommodation_crud = AccommodationCRUD(db)
  

  def create_accommodation_type(self, accommodation_data: dict):
    return self.accommodation_crud.create_accommodation_type(
      accommodation_data
    )
  
  def accommodation_type_list(self):
    return self.accommodation_crud.accommodation_type_list()