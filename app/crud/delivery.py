# setting up crud operations for package endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schema, models
from app.crud import packages as package_crud

#Implement service for creating, updating and retrieving deliveries.

# ## creating delivery methods
def create_delivery(package_id: int, payload: schema.DeliveryCreate, current_user: int, db: Session = Depends()) -> models.Delivery:

    # ## validate package availability
    package = package_crud.get_package_by_id(package_id, db)
    if not package:
        return None
    
    new_delivery = models.Delivery(**payload.model_dump(), user_id=current_user, package_id=package.id)
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery

