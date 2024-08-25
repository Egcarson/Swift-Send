from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import database, schema, oauth2
from app.crud import users as user_crud
from app.crud import addresses as address_crud

router = APIRouter(
    tags=["Address"]
)

# ## create user addresses


@router.post('/address', status_code=status.HTTP_201_CREATED, response_model=schema.Address)
def create_user_address(address_payload: schema.AddressCreate, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    existing_address = address_crud.get_address_by_id(user_id=current_user.id, db=db)
    # Checking if the user haven't added address already
    if existing_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an address"
        )
    
    new_address = address_crud.create_address(user_id=current_user.id, address_payload=address_payload, db=db)
    return new_address

# Get User addresses

@router.get('/address', response_model=schema.Address)
def get_user_addresses(db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    user = user_crud.get_user_by_id(id=current_user.id, db=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    address = address_crud.get_address_by_id(user_id=current_user.id, db=db)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found for this user")   
    return address

# update user address

@router.put('/addresses/{address_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Address)
def update_user_address(address_payload: schema.AddressUpdate, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    user = user_crud.get_user_by_id(id=current_user.id, db=db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    address = address_crud.get_address_by_id(user_id=current_user.id, db=db)
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found for this user"
        )
    
    updated_address = address_crud.update_address(user_id=current_user.id, address_payload=address_payload, db=db)
    
    return updated_address
