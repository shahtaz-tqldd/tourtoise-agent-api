from destination.db.crud import TransportCRUD

class TransportTypeService:
  def __init__(self, db):
    self.db = db
    self.transport_crud = TransportCRUD(db)

  def create_transport_type(self, transport_data: dict):
    return self.transport_crud.create_transport_type(
      transport_data
    )
  
  def transport_type_list(self):
    return self.transport_crud.transport_type_list()