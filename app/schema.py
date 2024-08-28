from pydantic import BaseModel, ConfigDict, EmailStr, condecimal, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
# from app.models import UserFunc


class UserFunc(str, Enum):
    CUSTOMER = "customer"
    COURIER = "courier"
    ADMIN = "admin"


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    DEBIT_CARD = "debit_card"
    PAYSTACK = "paystack"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"

# user schema:


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = "09034793278"
    city: Optional[str] = "Lagos"

class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    role: UserFunc
    is_active: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    first_name: str
    last_name: str

# ## schema for Token Generation
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ## schema for password rest
class PassReset(BaseModel):
    email: EmailStr
    new_password: str
    confirm_password: str

# ## schema for address


class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    zip_code: str
    country: str  # pulling from pycountry


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

# ## schema for Packages


class PackageBase(BaseModel):
    item_name: str
    weight: float
    dimensions: Optional[str] = None
    description: Optional[str] = None


class PackageCreate(PackageBase):
    pass


class PackageUpdate(PackageBase):
    pass


class Package(PackageBase):
    id: int
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)

class PackageResponse(PackageBase):
    id: int

# ## schema for Delivery


class DeliveryBase(BaseModel):
    payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
    pickup_address_id: int
    delivery_address_id: int
    created_at: datetime


class DeliveryCreate(DeliveryBase):
    pass

class DeliveryStatusUpdate(BaseModel):
    delivery_status: DeliveryStatus = DeliveryStatus.PENDING
    updated_at: datetime


class DeliveryUpdate(DeliveryBase):
    pass


class DeliveryCostUpdate(BaseModel):
    service_cost: Optional[condecimal(max_digits=10, decimal_places=2)] = "0.00" # type: ignore
    updated_at: datetime


class Delivery(DeliveryBase):
    id: int
    user: UserResponse
    service_cost: Optional[condecimal(max_digits=10, decimal_places=2)] = "0.00"  # type: ignore
    package: PackageResponse
    pickup_address: Address
    delivery_address: Address
    updated_at: datetime
    delivery_status: DeliveryStatus = DeliveryStatus.PENDING

    model_config = ConfigDict(from_attributes=True)

# ## schema for Status


# class StatusBase(BaseModel):
#     status: DeliveryStatus


# class StatusCreate(StatusBase):
#     pass


# class Status(StatusBase):
#     id: int
#     user_id: int
#     updated_at: datetime
