from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import database, schema, oauth2
from app.crud import users as user_crud

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")
    
    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name == user_payload.password) or user_payload.phone_number == user_payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_user(user_payload, db)
    return new_user

# ## endpoint to create an admin user
@router.post('/signup/admin', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_admin(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")
    
    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name) == user_payload.password or user_payload.phone_number == user_payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_admin_user(user_payload, db)
    return new_user

@router.post('/signup/courier', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_courier(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")

    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name == user_payload.password) or user_payload.phone_number == user_payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_courier_user(user_payload, db)
    return new_user

# ## login endpoint
@router.post('/login', status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = user_crud.authenticate_user(payload.username, payload.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # ## create access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # ## return access token
    return {"access_token": access_token, "token_type": "Bearer"}


# ## change password
@router.put('/auth/password/reset', status_code=status.HTTP_202_ACCEPTED)
def password_reset(payload: schema.PassReset, db: Session = Depends(database.get_db)):
    user = user_crud.get_user_by_email(payload.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address provided")
    
    # checking if the user is sure about the password
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    # updating the user password
    user_crud.update_password(payload, db)

    return {"message": "Password updated successfully"}