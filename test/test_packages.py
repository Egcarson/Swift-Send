import pytest



@pytest.mark.parametrize("payload, expected_item_name", [
    ({"item_name": "MacBook Pro", "weight": 170.0,
      "dimensions": "63 x 160", "description": "Black"}, "MacBook Pro")
])
def test_create_package(client, setup_database, payload, expected_item_name):
    
    # Signup
    response = client.post("/signup/customer", json={"first_name": "test", "last_name": "app",
                          "email": "test@gmail.com", "phone_number": "09034793278", "city": "Lagos", "password": "password123"})
    assert response.status_code == 201

    # Authenticate and get token
    response = client.post(
        "/login", data={"username": "test@gmail.com",  "password": "password123"})
    
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    token = response.json()["access_token"]

    response = client.post(
        "/packages", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["item_name"] == expected_item_name


def test_get_packages(client, setup_database):
    response = client.get("/packages")

    assert response.status_code == 200
    data = response.json()

    assert all("item_name" in package for package in data)
    assert all("weight" in package for package in data)
    assert all("dimensions" in package for package in data)
    assert all("description" in package for package in data)


@pytest.mark.parametrize("package_id, wrong_id, expected_item_name, expected_weight, expected_description", [(1, 99, "MacBook Pro", 170.0, "Black")])
def test_get_package_by_id(client, setup_database, package_id, wrong_id, expected_item_name, expected_weight, expected_description):
    # Assert for invalid id
    response = client.get(f"/package/{wrong_id}")
    assert response.status_code == 404

    response = client.get(f"/package/{package_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["item_name"] == expected_item_name
    assert data["weight"] == expected_weight
    assert data["description"] == expected_description


@pytest.mark.parametrize("package_id, wrong_id", [
    ( "1", "99")
])
def test_update_package(client, setup_database, package_id, wrong_id):
    # Signup admin user
    response = client.post("/signup/admin", json={"first_name": "testadmin", "last_name": "app",
                                                  "email": "testadmin@gmail.com", "phone_number": "07041458948", "city": "Lagos", "password": "password123"})


    # Login to authenticate normal customer
    response = client.post(
        "/login", data={"username": "test@gmail.com",  "password": "password123"})
    assert response.status_code == 200
    customer_token = response.json()["access_token"]
    
    # Login to authenticate admin user
    response = client.post(
        "/login/", data={"username": "testadmin@gmail.com",  "password": "password123"})

    assert response.status_code == 200
    admin_token = response.json()["access_token"]

    update_payload = {"item_name": "Updated_Package", "weight": 190.0}

    # Test authentication
    response = client.put(f"/packages/{package_id}", json=update_payload)
    assert response.status_code == 401


    # Test authentication with wrong id
    response = client.put(f"/packages/{wrong_id}", json=update_payload,
                          headers={"Authorization": f"Bearer {customer_token}"})

    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Package not found"}
    

    # Test authenticated user can update package
    response = client.put(f"/packages/{package_id}", json=update_payload,
                          headers={"Authorization": f"Bearer {customer_token}"})

    assert response.status_code == 202
    data = response.json()
    assert data["item_name"] == update_payload["item_name"]
    assert data["weight"] == update_payload["weight"]

    # Test admin can update package

    admin_update_payload = {
        "item_name": "Admin_Updated_Package", "weight": 200.0}

    response = client.put(f"/packages/{package_id}", json=admin_update_payload,
                          headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 202
    data = response.json()
    assert data["item_name"] == admin_update_payload["item_name"]
    assert data["weight"] == admin_update_payload["weight"]
