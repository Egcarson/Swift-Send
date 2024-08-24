# setting up crud operations for user endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app import schema, models, utils

# ## function for creating a user
def create_user(user_payload: schema.UserCreate, db: Session = Depends()):
    hashed_password = utils.hash_password(password=user_payload.password)
    user_payload.password = hashed_password

    role_asign = schema.UserFunc.CUSTOMER

    new_user = models.User(**user_payload.model_dump())
    new_user.role = role_asign

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ## function to create an admin user
def create_admin_user(user_payload: schema.UserCreate, db: Session = Depends()):
    hashed_password = utils.hash_password(password=user_payload.password)
    user_payload.password = hashed_password

    role_asign = schema.UserFunc.ADMIN

    new_user = models.User(**user_payload.model_dump())
    new_user.role = role_asign
    new_user.is_active = True
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ## function to create courier/driver account
def create_courier_user(user_payload: schema.UserCreate, db: Session = Depends()):
    hashed_password = utils.hash_password(password=user_payload.password)
    user_payload.password = hashed_password

    role_asign = schema.UserFunc.COURIER

    new_user = models.User(**user_payload.model_dump())
    new_user.role = role_asign
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ## function for getting all users
def get_users(db: Session = Depends(), skip: int = 0, limit: int = 10, search: Optional[str] = ""):
    users = db.query(models.User).filter(models.User.last_name.contains(
        search) | models.User.first_name.contains(search)).offset(skip).limit(limit).all()
    return users

# ## function for getting a single user by id


def get_user_by_id(id: int, db: Session = Depends()):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return None
    return user

# ## function for updating a user




def update_user(id: int, user_payload: schema.UserUpdate, db: Session = Depends()):
    user = get_user_by_id(id, db)
    if not user:
        return None

    unpack_user = user_payload.model_dump(exclude_unset=False)

    for k, v in unpack_user.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user

# ## function for deleting a user


def delete_user(id: int, db: Session = Depends()):
    user = get_user_by_id(id, db)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user


def get_user_by_email(email: str, db: Session = Depends()):
    user_email = db.query(models.User).filter(
        models.User.email == email).first()
    if not user_email:
        return None
    return user_email

# ## validating user informations


def authenticate_user(email: str, password: str, db: Session = Depends()):
    user = get_user_by_email(email, db)
    if not user:
        return None
    if not utils.verify_password(password, user.password):
        return None
    return user

# ## updating user's password


def update_password(payload: schema.PassReset, db: Session = Depends()):
    user = get_user_by_email(payload.email, db)
    if not user:
        return None

    if payload.new_password != payload.confirm_password:
        return None

    hashed_password = utils.hash_password(password=payload.new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    return user

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

# delete user_address

def delete_address(user_id: int, db: Session):
    user_address = get_address_by_id(user_id, db)
    if not user_address:
        return None
    db.delete(user_address)
    db.commit()
    return {"message": "user address deleted"}
