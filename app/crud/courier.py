# setting up crud operations for addresses endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schema, models


# ## setting up crud operation for retrieving all available couriers
def get_available_couriers(offset: int, limit: int, db: Session = Depends()):

    user_role = schema.UserFunc.COURIER

    couriers = db.query(models.User).filter(models.User.role == user_role).offset(offset).limit(limit).all()

    return couriers