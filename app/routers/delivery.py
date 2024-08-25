from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import database, schema, models, oauth2
from app.crud import users as user_crud, packages as package_crud, delivery as delv_crud

router = APIRouter(
    tags=["Delivery"]
)

# ## endpoint for creating deliveries
@router.post('/deliveries', status_code=status.HTTP_201_CREATED, response_model=schema.Delivery)
def add_delivery(package_id: int, payload: schema.DeliveryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # ## validate package
    package = package_crud.get_package_by_id(package_id, db)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    # ## validating availability of addresses
    if not payload.pickup_address_id and not payload.delivery_address_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Addresses are required to create a delivery"
        )
    
    delivery = delv_crud.create_delivery(package_id, payload, current_user.id, db)

    
    
    return delivery

# ## endpoint for getting all deliveries