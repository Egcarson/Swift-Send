from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from app import database, schema
from app.crud import courier as c_crud

router = APIRouter(
    tags=["Available Couriers"]
)

# ## endpoint for retrieving available couriers
@router.get('/couriers', status_code=status.HTTP_200_OK, response_model=List[schema.User])
def get_available_couriers(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):

    available_couriers = c_crud.get_available_couriers(offset, limit, db)
    
    if not available_couriers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No available couriers at the moment. Please try again later.")

    return available_couriers