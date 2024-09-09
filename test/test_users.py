import pytest


@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password", [("test", "app", "test@gmail.com", "09034793278", "Lagos", "password123")])
def test_get_users(client, setup_database, first_name, last_name, email, phone_number, city, password):
    # Signup Users


    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name,
                          "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    response = client.post("/signup/admin", json={"first_name": "testadmin", "last_name": "app",
                                                     "email": "testadmin@gmail.com", "phone_number": "07041458948", "city": "Lagos", "password": "password123"})
    assert response.status_code == 201

    response = client.get("/users")

    assert response.status_code == 200
    data = response.json()

    assert all("first_name" in user for user in data)
    assert all("email" in user for user in data)
    assert all("last_name" in user for user in data)
    assert all("phone_number" in user for user in data)


@pytest.mark.parametrize("user_id, wrong_id, expected_first_name, expected_email, expected_last_name", [(1, 99, "test", "test@gmail.com", "app")])
def test_get_user_by_id(client, setup_database, user_id, wrong_id, expected_first_name, expected_email, expected_last_name):
    # Assert for invalid id
    response = client.get(f"/users/{wrong_id}")
    assert response.status_code == 404

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["first_name"] == expected_first_name
    assert data["email"] == expected_email
    assert data["last_name"] == expected_last_name



@pytest.mark.parametrize("email, password, user_id, wrong_id, another_user_id", [
    ("test@gmail.com", "password123", 1, 99, 2)
])
def test_update_user(client, setup_database, email, password, user_id, wrong_id, another_user_id):

    # Login to authenticate
    response = client.post(
        "/login/", data={"username": email,  "password": password})

    assert response.status_code == 200
    token = response.json()["access_token"]

    update_payload = {"first_name": "Updated", "last_name": "User"}

    # Test authentication
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 401

    # Test to update user not in db
    response = client.put(f"/users/{wrong_id}", json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "User not found"}
    

    response = client.put(f"/users/{user_id}", json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_payload["first_name"]
    assert data["last_name"] == update_payload["last_name"]


    # Test to see if an authenticated user can edit another_user (should throw a 401 because not authorized to do so)
    response = client.put(f"/users/{another_user_id}", json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Not authorized"}


@pytest.mark.parametrize("email, password, user_id, wrong_id, another_user_id", [("test@gmail.com", "password123", 1, 99, 2)])
def test_delete_user(client, setup_database, email, password, user_id, wrong_id, another_user_id):

    # Login to authenticate
    response = client.post(
        "/login/", data={"username": email,  "password": password})

    assert response.status_code == 200
    token = response.json()["access_token"]

    # Test for authentication
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 401

    # Test to delete user not in db
    response = client.delete(f"/users/{wrong_id}",
                             headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "User not found"}

    # Test if authenticated user can delete another user
    response = client.delete(f"/users/{another_user_id}",
                             headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Not authorized"}

    # Test Authenticated user can delete account
    response = client.delete(
        f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Successful"}
