from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.schema import UserFunc, DeliveryStatus, PaymentMethod
from app.database import Base


# class UserFunc(enum.Enum):
#     CUSTOMER = "customer"
#     COURIER = "courier"
#     ADMIN = "admin"


# class DeliveryStatus(enum.Enum):
#     PENDING = "pending"
#     PICKED_UP = "picked_up"
#     IN_TRANSIT = "in_transit"
#     DELIVERED = "delivered"
#     CANCELLED = "cancelled"


# class PaymentMethod(enum.Enum):
#     DEBIT_CARD = "debit_card"
#     PAYSTACK = "paystack"
#     BANK_TRANSFER = "bank_transfer"
#     CASH_ON_DELIVERY = "cash_on_delivery"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserFunc), nullable=False, default=UserFunc.CUSTOMER)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    address = relationship("Address", back_populates="user")
    deliveries = relationship("Delivery", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    user = relationship("User", back_populates="address")


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)
    dimensions = Column(String)
    description = Column(String)

    deliveries = relationship("Delivery", back_populates="package")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    delivery_status = Column(Enum(DeliveryStatus),
                             default=DeliveryStatus.PENDING)
    pickup_address_id = Column(
        Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)
    delivery_address_id = Column(
        Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)
    payment_method = Column(Enum(PaymentMethod),
                            default=PaymentMethod.CASH_ON_DELIVERY)
    service_cost = Column(Numeric(precision=10, scale=2))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), onupdate=text('now()'))

    user = relationship("User", back_populates="deliveries")
    package = relationship("Package", back_populates="deliveries")
    status = relationship("Status", back_populates="deliveries")
    pickup_address = relationship("Address", foreign_keys=[pickup_address_id])
    delivery_address = relationship(
        "Address", foreign_keys=[delivery_address_id])


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(DeliveryStatus))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), onupdate=text('now()'))

    deliveries = relationship("Delivery", back_populates="status")
