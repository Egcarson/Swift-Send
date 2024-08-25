import os
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app import schema

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRATION_TIME = 30

# ## access token
def create_access_token(data: dict, expire_lift: Optional[timedelta] = None):
    to_encode = data.copy()

    if expire_lift:
        expire = datetime.now(timezone.utc) + expire_lift
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ## verifying access token
def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str = payload.get("user_id")

        if not user:
            raise credential_exception
        decoded_token = schema.TokenData(id=str(user)) #if this throws an error cast the user to str
     
    except JWTError as e:
        print(e)
        raise credential_exception
    return decoded_token


# ## authenticate user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to access this information.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    return verify_access_token(token, credential_exception)