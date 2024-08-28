# setting up crud operations for package endpoints
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schema, models


# ## package creation
def create_package(payload: schema.PackageCreate, current_user: int, db: Session = Depends()) -> models.Package:
    new_package = models.Package(**payload.model_dump(), user_id=current_user)
    db.add(new_package)
    db.commit()
    db.refresh(new_package)

    return new_package

# ## retrieving all packages
def get_packages(offset: int = 0, limit: int = 10, db: Session = Depends()) -> models.Package:
    return db.query(models.Package).offset(offset).limit(limit).all()

# ## retrieving package by id
def get_package_by_id(package_id: int, db: Session = Depends()) -> models.Package:
    return db.query(models.Package).filter(models.Package.id == package_id).first()

# ## package updating
def update_package(package_id: int, payload: schema.PackageUpdate, db: Session = Depends()) -> models.Package:
    package = get_package_by_id(package_id, db)
    if not package:
        return None

    unpack = payload.model_dump(exclude_unset=True)

    for k, v in unpack.items():
        setattr(package, k, v)
    db.commit()
    db.refresh(package)
    return package

# ## deleting packages
def delete_package(package_id: int, db: Session = Depends()):
    package = get_package_by_id(package_id, db)
    if not package:
        return None
    db.delete(package)
    db.commit()
    return package