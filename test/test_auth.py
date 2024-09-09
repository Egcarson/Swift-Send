from concurrent.futures.thread import _python_exit
import pytest

@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role", [("test", "app", "test@gmail.com", "09034793278", "Lagos", "password123", "091233", "pass", "customer")])
def test_signup_customer(client, setup_database, first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role):

    # ## phone number validation
    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": wrong_number, "city": city, "password": password})
  
    if len(wrong_number) != 11:
        assert response.status_code == 400
    
    ## testing password validation
    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": first_name})

    if first_name == password: 
        assert response.status_code == 400

    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": last_name})

    if last_name == password:
        assert response.status_code == 400

    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": short_password})
    
    if len(password) < 8:
        assert response.status_code == 400

    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": "testapp"})
    
    if password == (first_name + last_name):
        assert response.status_code == 400

    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": phone_number})
    
    if password == phone_number:
        assert response.status_code == 400
    
    # ## creating a user
    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == first_name
    assert data["role"] == role


    # ## test for conflict - user already exists
    response = client.post("/signup/customer", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 409


@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role", [("testadmin", "app", "testadmin@gmail.com", "09034793276", "Lagos", "password123", "091233", "pass", "admin")])
def test_signup_admin(client, setup_database, first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role):

    # ## phone number validation
    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": wrong_number, "city": city, "password": password})

    if len(wrong_number) != 11:
        assert response.status_code == 400

    # testing password validation
    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": first_name})

    if first_name == password:  
        assert response.status_code == 400

    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": last_name})

    if last_name == password:
        assert response.status_code == 400

    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": short_password})

    if len(password) < 8:
        assert response.status_code == 400

    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": "testadminapp"})

    if password == (first_name + last_name):
        assert response.status_code == 400

    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": phone_number})

    if password == phone_number:
        assert response.status_code == 400

    # ## creating a admin user
    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == first_name
    assert data["role"] == role

    # ## test for conflict - user already exists
    response = client.post("/signup/admin", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 409


@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role", [("testcourier", "app", "testcourier@gmail.com", "09034793271", "Lagos", "password123", "091233", "pass", "courier")])
def test_signup_courier(client, setup_database, first_name, last_name, email, phone_number, city, password, wrong_number, short_password, role):

    # ## phone number validation
    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": wrong_number, "city": city, "password": password})

    if len(wrong_number) != 11:
        assert response.status_code == 400

    # testing password validation
    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": first_name})

    if first_name == password:  
        assert response.status_code == 400

    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": last_name})

    if last_name == password:
        assert response.status_code == 400

    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": short_password})

    if len(password) < 8:
        assert response.status_code == 400

    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": "testcourierapp"})

    if password == (first_name + last_name):
        assert response.status_code == 400

    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": phone_number})

    if password == phone_number:
        assert response.status_code == 400

    # ## creating a admin user
    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == first_name
    assert data["role"] == role

    # ## test for conflict - user already exists
    response = client.post("/signup/courier", json={"first_name": first_name, "last_name": last_name,
                           "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 409


# Test Login

@pytest.mark.parametrize("email, password", [("test@gmail.com", "password123")])
def test_login(client, setup_database, email, password):

    # Login
    response = client.post(
        "/login", data={"username": email,  "password": password})

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    # Test Login with wrong email
    response = client.post(
        "/login", data={"username": "wrongtest@gmail.com",  "password": password})

    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Incorrect username or password"}

    # Test Login with incorrect password
    response = client.post(
        "/login/", data={"username": "testadmin@gmail.com",  "password": "wrong_password"})

    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Incorrect username or password"}


@pytest.mark.parametrize("email, password, new_password, confirm_password, first_name, last_name, phone_number, short_password", [("test@gmail.com", "password123", "password1234", "password1234", "test", "app", "09034793278", "pass")])
def test_password_reset(client, setup_database, email, password, new_password, confirm_password, first_name, last_name, phone_number, short_password):

    # Login

    response = client.post(
        "/login/", data={"username": email,  "password": password})

    assert response.status_code == 200
    token = response.json()["access_token"]

    # Login another user to check for authentication

    response = client.post(
        "/login/", data={'username': 'testadmin@gmail.com',  'password': password})

    assert response.status_code == 200
    admin_token = response.json()["access_token"]
   

    # Test update password with wrong email 
    update_payload = {'email': 'wrong_email@gmail.com', 'new_password': new_password, 'confirm_password': confirm_password}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 404

    # Test update password of another user (should throw not authenticated)
    update_payload = {'email': 'test@gmail.com',
                      'new_password': new_password, 'confirm_password': confirm_password}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 401
    
    # Test update password new password does not match confirm password
    update_payload = {'email': 'test@gmail.com',
                      'new_password': new_password, 'confirm_password': 'password_mismatch'}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "Passwords do not match"}

    # Test update password new password same as old password
    update_payload = {'email': 'test@gmail.com',
                      'new_password': password, 'confirm_password': password}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "This is your previous password. Please use something stronger"}
    
    # Test update password new password same as first name
    update_payload = {'email': 'test@gmail.com',
                      'new_password': first_name, 'confirm_password': first_name}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "Password is too weak! Please make it stronger for security reasons."}
    
    # Test update password new password same as last name
    update_payload = {'email': 'test@gmail.com',
                      'new_password': last_name, 'confirm_password': last_name}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "Password is too weak! Please make it stronger for security reasons."}
    
    # Test update password new password same as phone number
    update_payload = {'email': 'test@gmail.com',
                      'new_password': phone_number, 'confirm_password': phone_number}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "Password is too weak! Please make it stronger for security reasons."}
    
    # Test update password new password same as first name and last name combined
    update_payload = {'email': 'test@gmail.com',
                      'new_password': (first_name + last_name), 'confirm_password': (first_name + last_name)}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "Password is too weak! Please make it stronger for security reasons."}

    # Test update password new password is shorter than 8 characters
    update_payload = {'email': 'test@gmail.com',
                      'new_password': short_password, 'confirm_password': short_password}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 400
    data = response.json()
    assert data == {
        "detail": "Password is too weak! Please make it stronger for security reasons."}
    
    # Test update password
    update_payload = {'email': 'test@gmail.com',
                      'new_password': new_password, 'confirm_password': confirm_password}

    response = client.put('/auth/password/reset', json=update_payload,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 202
    
