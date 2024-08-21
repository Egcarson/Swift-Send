from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# user schema:
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    city: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool = False

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class PassReset(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str


class TokenData(BaseModel):
    id: Optional[str] = None