from destination.db.crud import ActivityCRUD

class ActivityTypeService:
  def __init__(self, db):
    self.db = db
    self.activity_crud = ActivityCRUD(db)

  def create_activity_type(self, activity_data: dict):
    return self.activity_crud.create_activity_type(
      activity_data
    )
  
  def activity_type_list(self):
    return self.activity_crud.activity_type_list()