# setting up crud operations for addresses endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app import schema, models, utils


# ## setting up crud operations for address endpoint for user


# create a new address for user
def create_address(address_payload: schema.AddressCreate, db: Session, user_id: int ):
    user_address = models.Address( user_id=user_id,**address_payload.model_dump())
    db.add(user_address)
    db.commit()
    db.refresh(user_address)
    return user_address

# get address from db by user_id

def get_address_by_id(user_id: int, db: Session):
    user_address = db.query(models.Address).filter(models.Address.user_id == user_id).first()
    if not user_address:
        return None
    return user_address


# update user_address

def update_address(user_id: int, address_payload: schema.AddressUpdate, db: Session):
    user_address = get_address_by_id(user_id, db)
    if not user_address:
        return None
    unpack_address = address_payload.model_dump(exclude_unset=False)
    for k, v in unpack_address.items():
        setattr(user_address, k, v)
    db.commit()
    db.refresh(user_address)
    return user_address


