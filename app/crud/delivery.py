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

def get_deliveries(offset: int, limit: int, db: Session = Depends()) -> models.Delivery:
    return db.query(models.Delivery).offset(offset).limit(limit).all()

def get_delivery_by_id(id: int, db: Session = Depends()) -> models.Delivery:
    delivery_query = db.query(models.Delivery).filter(models.Delivery.id == id)
    delivery = delivery_query.first()
    if not delivery:
        return None
    return delivery

def get_delivery_by_package_id(package_id: int, db: Session = Depends()) -> models.Delivery:
    delivery = db.query(models.Delivery).filter(models.Delivery.package_id == package_id).first()
    if not delivery:
        return None
    return delivery

def update_delivery(delivery_id: int, payload: schema.DeliveryUpdate, db: Session = Depends()) -> models.Delivery:
    delivery = get_delivery_by_id(delivery_id, db)
    
    delivery_dict = payload.model_dump(exclude_unset=True)

    for k, v in delivery_dict.items():
        setattr(delivery, k, v)
    db.commit()
    db.refresh()

    return delivery
    
# ## cancel delivery
def cancel_delivery(delivery_id: int, db: Session = Depends()) -> models.Delivery:
    delivery = get_delivery_by_id(delivery_id, db)
    if not delivery:
        return None
    
    delivery.delivery_status = schema.DeliveryStatus.CANCELLED
    db.commit()
    db.refresh(delivery)
    return delivery


# ## status update
def update_delivery_status(delivery_id: int, payload: schema.DeliveryStatusUpdate, db: Session = Depends()):
    delivery = get_delivery_by_id(delivery_id, db)
    if not delivery:
        return None
    
    ## updating status
    status = payload.model_dump(exclude_unset=True)

    for k, v in status.items():
        setattr(delivery, k, v)
    db.commit()
    db.refresh(delivery)

    return delivery

# ## delivery fee update
def update_delivery_fee(delivery_id: int, payload: schema.DeliveryCostUpdate, db: Session = Depends()):
    delivery = get_delivery_by_id(delivery_id, db)
    if not delivery:
        return None
    
    ## updating status
    status = payload.model_dump(exclude_unset=True)

    for k, v in status.items():
        setattr(delivery, k, v)
    db.commit()
    db.refresh(delivery)

    return delivery