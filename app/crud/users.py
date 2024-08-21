# setting up crud operations for user endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional
from app import schema, models, utils

# ## function for creating a user


def create_user(user_payload: schema.UserCreate, db: Session = Depends()):
    hashed_password = utils.hash_password(password=user_payload.password)
    user_payload.password = hashed_password
    new_user = models.User(**user_payload.model_dump())
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
