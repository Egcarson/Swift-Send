from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import database, schema, oauth2
from app.crud import users as user_crud
from app.crud import addresses as address_crud
from app.logs.logger import get_logger

router = APIRouter(
    tags=["Address"]
)

logger = get_logger()

# ## create user addresses
@router.post('/address', status_code=status.HTTP_201_CREATED, response_model=schema.Address)
def create_user_address(address_payload: schema.AddressCreate, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    
    new_address = address_crud.create_address(user_id=current_user.id, address_payload=address_payload, db=db)
    logger.info("New address created")
    return new_address

## retrieving all addresses created by a user
@router.get('/address', status_code=status.HTTP_200_OK, response_model=List[schema.Address])
def get_all_addresses(offset:int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    user = user_crud.get_user_by_id(user_id, db)
   
    addresses = address_crud.get_addresses(offset, limit, user.id, db)
    return addresses

# Get User addresses
@router.get('/address/{address_id}', status_code=status.HTTP_200_OK, response_model=schema.Address)
def get_user_address(address_id: int, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):

    user_id = current_user.id
    user = user_crud.get_user_by_id(user_id, db)

    ## validate availability of address
    address = address_crud.get_address_by_id(address_id, user.id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Adress not found"
        )

    address = address_crud.get_address_by_id(user_id=current_user.id, db=db)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found for this user")   
    return address

# update user address

@router.put('/addresses/{address_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Address)
def update_user_address(address_id: int, address_payload: schema.AddressUpdate, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    
    user_id = current_user.id
    user = user_crud.get_user_by_id(user_id, db)
    
    ## validate availability of address
    address = address_crud.get_address_by_id(address_id, user.id, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please specify the right address id belonging to you!"
        )
    
    updated_address = address_crud.update_address(address_id, address_payload, user.id, db)
    
    return updated_address

# ## delete address
@router.delete('/address/{address_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_address(address_id: int, db: Session = Depends(database.get_db), current_user: schema.User = Depends(oauth2.get_current_user)):
    
    user_id = current_user.id
    user = user_crud.get_user_by_id(user_id, db)
    
    ## validate availability of address
    address = address_crud.get_address_by_id(address_id, user.id, db)
    
    if not address:
        logger.error("Address not found for this user")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please specify the right address id belonging to you!"
        )
    
    updated_address = address_crud.update_address(user_id=current_user.id, address_payload=address_payload, db=db)
    
    return updated_address
