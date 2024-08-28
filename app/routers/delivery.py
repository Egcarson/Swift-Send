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
    if not payload.pickup_address_id or not payload.delivery_address_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Addresses are required to create a delivery"
        )

    # ## validate availability of delivery before creating another one
    delivery = delv_crud.get_delivery_by_package_id(package_id, db)
    if delivery:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Delivery for this package has been processed already"
        )

    # ## create delivery
    delivery = delv_crud.create_delivery(
        package_id, payload, current_user.id, db)

    return delivery

# ## endpoint for getting all deliveries
@router.get('/deliveries', status_code=status.HTTP_200_OK, response_model=List[schema.Delivery])
def get_deliveries(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    deliveries = delv_crud.get_deliveries(offset, limit, db)
    return deliveries

# ## getting delivery by id to check the status
@router.get('/deliveries/{delivery_id}', status_code=status.HTTP_200_OK, response_model=schema.Delivery)
def get_delivery_by_id(delivery_id: int, db: Session = Depends(database.get_db)):

    # ### validate availability of delivery
    delivery = delv_crud.get_delivery_by_id(delivery_id, db)

    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, there is no delivery available"
        )
    
    return delivery


# ## for updating delivery information
@router.put('/deliveries/{delivery_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Delivery)
def update_delivery(delivery_id: int, payload: schema.DeliveryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    # ## validating the availability of requested delivery id
    delivery = delv_crud.get_delivery_by_id(delivery_id, db)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error! The delivery info you requested does not exist"
        )

    # ## validate user
    if delivery.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to edit the requested information."
        )

    delivery_update = delv_crud.update_delivery(delivery.id, payload, db)

    return delivery_update

# ## cancel delivery
@router.delete('/deliveries/{delivery_id}', status_code=status.HTTP_202_ACCEPTED)
def cancel_delivery(delivery_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    delivery = delv_crud.get_delivery_by_id(delivery_id, db)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error! The delivery you are trying to cancel does not exist"
        )
    
    # ## validate user - also allowing user that created the delivery to cancel it
    user = user_crud.get_user_by_id(current_user.id, db)
    
    if delivery.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to cancel this delivery."
        )
    
    # checking if the delivery has already been cancelled
    status_check = schema.DeliveryStatus.CANCELLED
    if delivery.delivery_status == status_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error! Delivery has already been cancelled."
        )
    
    # ## cancelling the delivery
    delv_crud.cancel_delivery(delivery_id, db)

    return {"message": "Delivery cancelled successfully!"}
    

## status endpoints
@router.put('/deliveries/status/{delivery_id}', status_code=status.HTTP_202_ACCEPTED)
def update_delivery_status(delivery_id: int, payload: schema.DeliveryStatusUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):


    # validating delivery
    delivery = delv_crud.get_delivery_by_id(delivery_id, db)
    
    if not delivery:
        raise HTTPException(
            status_code=404, 
            detail="The delivery information you are trying to update does not exist"
        )
    
    # ## enforcing update to be done by courier or admin users only
    user = user_crud.get_user_by_id(current_user.id, db)

    admin_user = schema.UserFunc.ADMIN
    courier_user = schema.UserFunc.COURIER

    if user.role != admin_user and user.role != courier_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Error! Please you are not allowed to perform this action."
        )
    
    delv_crud.update_delivery_status(delivery_id, payload, db)

    return {"message": "Status updated successfully!"}

# this endpoint is updating the delivery fee
@router.put('/deliveries/delivery_fee/{delivery_id}', status_code=status.HTTP_202_ACCEPTED)
def assign_delivery_fee(delivery_id: int, payload: schema.DeliveryCostUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):


    # validating delivery
    delivery = delv_crud.get_delivery_by_id(delivery_id, db)
    
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="The delivery information you are trying to update does not exist"
        )
    
    # ## enforcing update to be done by courier or admin users only
    user = user_crud.get_user_by_id(current_user.id, db)

    admin_user = schema.UserFunc.ADMIN
    courier_user = schema.UserFunc.COURIER

    if user.role != admin_user and user.role != courier_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Error! Please you are not allowed to perform this action."
        )
    
    delv_crud.update_delivery_fee(delivery_id, payload, db)

    return {"message": "Delivery price successfully added"}
