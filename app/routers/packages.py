from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from app import database, schema, models, oauth2
from app.crud import users as user_crud, packages as package_crud

router = APIRouter(
    tags=["Packages"]
)

# ## endpoint for creating packages


@router.post('/packages', status_code=status.HTTP_201_CREATED, response_model=schema.Package)
def create_package(payload: schema.PackageCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    new_package = package_crud.create_package(payload, current_user.id, db)

    return new_package

# ## endpoint for retrieving all package


@router.get('/packages', status_code=status.HTTP_200_OK, response_model=List[schema.Package])
def get_packages(offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    packages = package_crud.get_packages(offset, limit, db)
    return packages


@router.get('/package/{package_id}', status_code=status.HTTP_200_OK, response_model=schema.Package)
def get_package_by_id(package_id, db: Session = Depends(database.get_db)):
    package = package_crud.get_package_by_id(package_id, db)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    return package

# ## endpoint for updating packages
@router.put('/packages/{package_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schema.Package)
def update_package(package_id: int, payload: schema.PackageUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    package = package_crud.get_package_by_id(package_id, db)
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # ## allowing admin users to edit the package
    admin_role = schema.UserFunc.ADMIN
    user = user_crud.get_user_by_id(current_user.id, db)

    if user.role == admin_role:
        # ## update package
        updated_package = package_crud.update_package(package_id, payload, db)
        return updated_package

    # ## only user that created a package is allowed to edit a package
    if package.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action!. Thank you."
        )
    
    # ## update package
    updated_package = package_crud.update_package(package_id, payload, db)
    return updated_package
