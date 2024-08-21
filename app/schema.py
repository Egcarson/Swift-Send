import enum
from pydantic import BaseModel, ConfigDict, EmailStr, condecimal
from typing import Optional
from datetime import datetime


class UserRole(str, enum):
    CUSTOMER = "customer"
    COURIER = "courier"
    ADMIN = "admin"


class DeliveryStatus(str, enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum):
    DEBIT_CARD = "debit_card"
    PAYSTACK = "paystack"
    BANK_TRANSFER = "bank_transfer"
    CASH_ON_DELIVERY = "cash_on_delivery"

# user schema:


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    city: str
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


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
    user_id: int
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
    user_id: int

# ## schema for Delivery


class DeliveryBase(BaseModel):
    payment_method: PaymentMethod = PaymentMethod.CASH_ON_DELIVERY
    created_at: datetime


class DeliveryCreate(DeliveryBase):
    package_id: int
    pickup_address_id: int
    delivery_address_id: int


class DeliveryUpdate(DeliveryBase):
    service_cost: condecimal(max_digits=10, decimal_places=2)  # type: ignore
    updated_at: datetime


class Delivery(DeliveryBase):
    id: int
    user_id: int
    package: Package
    pickup_address: Address
    delivery_address: Address
    delivery_status: DeliveryStatus = DeliveryStatus.PENDING


# ## schema for Status

class StatusBase(BaseModel):
    status: DeliveryStatus


class StatusCreate(StatusBase):
    delivery_id: int


class Status(StatusBase):
    id: int
    updated_at: datetime
