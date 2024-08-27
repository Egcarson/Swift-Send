from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import database, schema, oauth2, utils
from app.crud import users as user_crud
from app.logs.logger import get_logger

router = APIRouter(
    tags=["Authentication"]
)

logger = get_logger()

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        logger.warning(f'user with the email {user_payload.email} already exists')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")
    
    
    # validating phone number
    phone_number = user_payload.phone_number
    if len(phone_number) != 11:
        logger.error("Invalid phone number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Please enter a valid 11-digit phone number."
        )
    
    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name == user_payload.password) or user_payload.phone_number == user_payload.password:
        logger.info("Password is too weak")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_user(user_payload, db)
    logger.info("New user created")
    return new_user

# ## endpoint to create an admin user
@router.post('/signup/admin', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_admin(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        logger.warning(f'user with the email {user_payload.email} already exists')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")

    # validating phone number
    phone_number = user_payload.phone_number
    if len(phone_number) != 11:
        logger.error("Invalid phone number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Please enter a valid 11-digit phone number."
        )
    
    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name) == user_payload.password or user_payload.phone_number == user_payload.password:
        logger.info("Password is too weak")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_admin_user(user_payload, db)
    logger.info("New user created")
    return new_user

@router.post('/signup/courier', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_courier(user_payload: schema.UserCreate, db: Session = Depends(database.get_db)):

    #checking if the user exists or the email have been used already
    user_email = user_crud.get_user_by_email(user_payload.email, db)
    if user_email:
        logger.warning(f'user with the email {user_payload.email} already exists')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists")
    
    # validating phone number
    phone_number = user_payload.phone_number
    if len(phone_number) != 11:
        logger.error("Invalid phone number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Please enter a valid 11-digit phone number."
        )

    ## setting up a password check instance
    if user_payload.first_name == user_payload.password or user_payload.last_name == user_payload.password or len(user_payload.password) == 7 or (user_payload.first_name + user_payload.last_name == user_payload.password) or user_payload.phone_number == user_payload.password:
        logger.info("Password is too weak")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # initializing a new user
    new_user = user_crud.create_courier_user(user_payload, db)
    logger.info("New courier created")
    return new_user

# ## login endpoint
@router.post('/login', status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = user_crud.authenticate_user(payload.username, payload.password, db)
    if not user:
        logger.error("Incorrect username or password provided")
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
        logger.error(f'user with the email {payload.email} not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email address provided")
    
    # checking if the user is sure about the password
    if payload.new_password != payload.confirm_password:
        logger.error("Passwords do not match")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    # checking if the user is trying to resue thesame password
    if utils.verify_password(payload.new_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This is your previous password. Please use something stronger")
    
    ## setting up a password check instance
    if user.first_name == payload.new_password or user.last_name == payload.new_password or len(payload.new_password) == 7 or (user.first_name + user.last_name == payload.new_password) or user.phone_number == payload.new_password:
        logger.info("Password is too weak")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too weak! Please make it stronger for security reasons."
        )
    
    # updating the user password
    user_crud.update_password(payload, db)
    logger.info(f"Password updated for user with email: {payload.email}")
    return {"message": "Password updated successfully"}