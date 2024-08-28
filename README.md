
# SWIFT SEND

Welcome to SWIFT SEND, a delivery application designed to make sending and receiving packages simple, fast, and reliable. Whether you're shipping across the city or across the country, SWIFT SEND ensures your package gets there swiftly and safely.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Endpoints Overview](#endpoints-overview)
    - [Authentication Endpoints](#authentication-endpoints)
    - [Address Endpoints](#address-endpoints)
    - [Package Endpoints](#package-endpoints)
    - [Delivery Endpoints](#delivery-endpoints)
4. [Enums Used in the API](#enums-used-in-the-api)
5. [Credits](#credits)

## Introduction

**SWIFT SEND** is developed using FastAPI, a modern and high-performance web framework for Python. This API supports comprehensive delivery management operations including user authentication, address management, package creation, and delivery tracking, making it ideal for any delivery-based application.

### Shout Out to Altschool!

A big shout-out to **Altschool** for providing an exceptional platform that nurtures and develops tech talents. Their comprehensive and extensive training program equips aspiring developers with the necessary skills and knowledge to excel in the tech industry. **Altschool**'s commitment to hands-on learning, mentorship, and community support has prepared us to confidently tackle any challenges and resolve complex issues within the tech space. We are proud to be a part of this vibrant learning community that fosters innovation, creativity, and a passion for technology. This **API** was built by **Godprevail Eseh** and **Olalere Sherifdeen Abiodun**, two dedicated developers from the Altschool community..

## Installation

To set up and run the SWIFT SEND API locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/swift-send.git
   cd swift-send
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python -m venv env
    `env\Scripts\activate` # on Mac source env/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   uvicorn app.main:app --reload
   ```

Access the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints Overview

Below is an overview of the endpoints provided by the SWIFT SEND API.

### Authentication Endpoints

1. **Signup**: Register a new user.
   - **User Endpoint:** `POST /signup`
   - **Admin Endpoint:** `POST /signup/admin`
   - **Courier Endpoint:** `POST /signup/courier`

2. **Login**: Authenticate a user and provide an access token.
   - **Endpoint:** `POST /login`

### Address Endpoints

1. **Create Address**: Add a new address for deliveries.
   - **Endpoint:** `POST /addresses`

2. **Get Address**: Retrieve details of an address.
   - **Endpoint:** `GET /addresses/{address_id}`

3. **Update Address**: Modify existing address information.
   - **Endpoint:** `PUT /addresses/{address_id}`

4. **Delete Address**: Remove an address.
   - **Endpoint:** `DELETE /addresses/{address_id}`

### Package Endpoints

1. **Create Package**: Register a new package for delivery.
   - **Endpoint:** `POST /packages`

2. **Get Package**: Retrieve details of a specific package.
   - **Endpoint:** `GET /packages/{package_id}`

3. **Update Package**: Update details of a package.
   - **Endpoint:** `PUT /packages/{package_id}`

4. **Delete Package**: Remove a package from the system.
   - **Endpoint:** `DELETE /packages/{package_id}`

### Delivery Endpoints

1. **Create Delivery**: Schedule a new delivery for a package.
   - **Endpoint:** `POST /deliveries`

2. **Get Delivery**: Retrieve delivery details including status and addresses.
   - **Endpoint:** `GET /deliveries/{delivery_id}`

3. **Update Delivery Status**: Update the status of a delivery (admin/courier priviledge only) - (e.g., PENDING, DELIVERED).
   - **Endpoint:** `PUT /deliveries/{delivery_id}/status`

4. **Cancel Delivery**: Cancel a scheduled delivery.
   - **Endpoint:** `DELETE /deliveries/{delivery_id}`

5. **Assign Delivery Fee**: Assign a fee to a scheduled delivery (admin/courier priviledge only).
   - **Endpoint:** `DELETE /deliveries/{delivery_id}`

## Enums Used in the API

Enums are used to define a set of named values that represent different statuses or methods in the API. Here are the enums used in SWIFT SEND:

### Delivery Status Enum

Defines the current state of a delivery.

```python
class DeliveryStatus(str, Enum):
    PENDING = "pending"               # The package is awaiting pickup.
    PICKED_UP = "picked_up"           # The package has been picked up by the courier.
    IN_TRANSIT = "in_transit"         # The package is on its way to the delivery address.
    DELIVERED = "delivered"           # The package has been delivered to the recipient.
    CANCELLED = "cancelled"           # The delivery has been cancelled.
```

### Payment Method Enum

Specifies the payment method for the delivery service.

```python
class PaymentMethod(str, Enum):
    DEBIT_CARD = "debit_card"          # Payment will be made using a debit card.
    PAYSTACK = "paystack"              # Payment will be processed through Paystack, an online payment platform.
    BANK_TRANSFER = "bank_transfer"    # Payment will be made via a direct bank transfer.
    CASH_ON_DELIVERY = "cash_on_delivery"  # Payment will be made in cash when the package is delivered.
```


## Credits

Developed by **Godprevail Eseh** and **Olalere Sherifdeen Abiodun**.

A big thank you to **Altschool** for their support and educational platform that made this project possible.

Feel free to explore, test, and provide feedback! THANKS
