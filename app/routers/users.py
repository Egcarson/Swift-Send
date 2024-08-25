from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import database, schema, oauth2
from app.crud import users as user_crud

router = APIRouter(
    tags=["Users"]
)

# router.post('/users', status_code=status.HTTP_201_CREATED,
#             response_model=schema.User)
# def create_user(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):
#     new_user = user_crud.create_user(user_payload, db)
#     return new_user

# ## retrieving all users


@router.get('/users', response_model=List[schema.User])
def get_users(skip: int = 0, limit: int = 10, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    users = user_crud.get_users(skip=skip, limit=limit, search=search, db=db)
    return users

# ## retrieving user by id


@router.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# ## updating user


@router.put('/users/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.User)
def update_user(user_id: int, user_payload: schema.UserUpdate, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_update = user_crud.update_user(user_id, user_payload, db)
    return user_update

# ## deleting user


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_crud.delete_user(user_id, db)