import pytest

@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password", [("test", "app", "test@gmail.com", "09034793278", "Lagos", "password123")])
def test_signup(client, setup_database, first_name, last_name, email, phone_number, city, password):

    # ## phone number validation
    new_phone = "090347932"
    response = client.post("/signup", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": new_phone, "city": city, "password": password})
  
    if len(new_phone) != 11:
        assert response.status_code == 400
    
    ## testing password validation
    response = client.post("/signup", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})

    if first_name == password or last_name == password or len(password) < 8 or (first_name + last_name == password) or phone_number == password:
        assert response.status_code == 400
    
    # ## creating a user
    response = client.post("/signup", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == first_name

    # ## test for conflict - user already exists
    response = client.post("/signup", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 409

    