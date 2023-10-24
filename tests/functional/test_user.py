def test_create_user(client):
    data = {
        "username": "myusername",
        "password": "mypassword",
        "email": "myemail@test.com"
    }
    response = client.post('/api/users/', json=data)

    assert response.status_code == 201

    data_json = response.get_json()
    assert data_json['username'] == data['username']
    assert data_json['email'] == data['email']
    assert data_json['is_admin'] == False

def test_create_user_invalid(client):
    data = {
        "username": "myus *ername",
        "password": "my pass #word",
        "email": "myemail"
    }
    response = client.post('/api/users/', json=data)

    assert response.status_code == 400

    data_json = response.get_json()
    assert data_json['errors']['username'] == 'username must only contain letters, numbers and underscores.'
    assert data_json['errors']['password'] == 'password must only contain letters, numbers and underscores.'
    assert data_json['errors']['email'] == 'Not a valid email address.'

def test_create_user_email_or_username_exists(client, user_regular_fixture):
    data = {
        "username": "myusername",
        "password": "mypassword",
        "email": "user@test.com"
    }
    response = client.post('/api/users/', json=data)

    assert response.status_code == 400

    data_json = response.get_json()
    assert data_json['errors']['username'] == 'this username already exists'
    assert data_json['errors']['email'] == 'this email already exists'

def test_list_all_users_for_admin(client, headers_user_admin_fixture, user_regular_fixture):
    response = client.get('/api/users/', headers=headers_user_admin_fixture)
    assert response.status_code == 200

    data_json = response.get_json()
    assert len(data_json) == 2

def test_list_all_users_regular_user(client, headers_regular_user_fixture):
    response = client.get('/api/users/', headers=headers_regular_user_fixture)
    assert response.status_code == 403

def test_list_all_users_without_credentials(client, user_regular_fixture):
    response = client.get('/api/users/')
    assert response.status_code == 401

def test_get_user_for_current_user(client, headers_regular_user_fixture, user_regular_fixture):
    response = client.get('/api/users/1', headers=headers_regular_user_fixture)

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['username'] == user_regular_fixture.username
    assert data_json['email'] == user_regular_fixture.email
    assert data_json['id'] == 1
    assert data_json['is_admin'] == False

def test_get_user_for_admin_user(client, headers_user_admin_fixture, user_regular_fixture):
    response = client.get('/api/users/2', headers=headers_user_admin_fixture)

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['username'] == user_regular_fixture.username
    assert data_json['email'] == user_regular_fixture.email
    assert data_json['id'] == 2
    assert data_json['is_admin'] == False

def test_get_user_not_found(client, headers_user_admin_fixture):
    response = client.get('/api/users/100', headers=headers_user_admin_fixture)
    assert response.status_code == 404

def test_get_user_for_another_user_not_admin(client, headers_regular_user_fixture, user_admin_fixture):
    response = client.get('/api/users/2', headers=headers_regular_user_fixture)
    assert response.status_code == 403

def test_get_user_without_credentials(client, user_regular_fixture):
    response = client.get('/api/users/1')
    assert response.status_code == 401

def test_update_user_for_current_user(client, headers_regular_user_fixture):
    data = {
        "username": "newusername",
        "email": "newemail@email.com"
    }
    response = client.put('/api/users/1', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['username'] == data['username']
    assert data_json['email'] == data['email']

def test_update_user_already_exists(client, headers_regular_user_fixture, user_admin_fixture):
    data = {
        "username": "user_admin",
        "email": "admin@test.com"
    }
    response = client.put('/api/users/1', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 400

    data_json = response.get_json()
    assert data_json['errors']['username'] == 'this username already exists'
    assert data_json['errors']['email'] == 'this email already exists'

def test_update_user_data_invalid(client, headers_regular_user_fixture):
    data = {
        "username": "my user &*",
        "email": "ola ola#"
    }
    response = client.put('/api/users/1', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 400

    data_json = response.get_json()
    assert data_json['errors']['username'] == 'username must only contain letters, numbers and underscores.'
    assert data_json['errors']['email'] == 'Not a valid email address.'

def test_update_user_for_admin_user(client, headers_user_admin_fixture, user_regular_fixture):
    data = {
        "username": "newusername",
        "email": "newemail@email.com"
    }
    response = client.put('/api/users/2', json=data, headers=headers_user_admin_fixture)

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['username'] == data['username']
    assert data_json['email'] == data['email']

def test_update_user_for_another_user(client, headers_regular_user_fixture, user_admin_fixture):
    data = {
        "username": "newusername",
        "email": "newemail@email.com"
    }
    response = client.put('/api/users/2', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 403

def test_update_user_not_found(client, headers_user_admin_fixture):
    data = {
        "username": "newusername",
        "email": "newemail@email.com"
    }
    response = client.put('/api/users/100', json=data, headers=headers_user_admin_fixture)

    assert response.status_code == 404

def test_delete_user_for_admin_user(client, headers_user_admin_fixture, user_regular_fixture):
    response = client.delete('/api/users/2', headers=headers_user_admin_fixture)
    assert response.status_code == 204

def test_delete_user_for_current_user(client, headers_regular_user_fixture):
    response = client.delete('/api/users/1', headers=headers_regular_user_fixture)
    assert response.status_code == 204

def test_delete_user_for_another_user(client, headers_regular_user_fixture, user_admin_fixture):
    response = client.delete('/api/users/2', headers=headers_regular_user_fixture)
    assert response.status_code == 403

def test_delete_user_without_credentials(client, user_admin_fixture):
    response = client.delete('/api/users/1')
    assert response.status_code == 401

def test_delete_user_for_admin_user(client, headers_user_admin_fixture, user_regular_fixture):
    response = client.delete('/api/users/100', headers=headers_user_admin_fixture)
    assert response.status_code == 404

def test_update_password_for_current_user(client, headers_regular_user_fixture):
    data = {
        "old_password": "mypassword",
        "new_password": "new_password"
    }
    response = client.post('/api/users/1/update_password', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 200

def test_update_password_password_wrong(client, headers_regular_user_fixture):
    data = {
        "old_password": "wrongepassword",
        "new_password": "new_password"
    }
    response = client.post('/api/users/1/update_password', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 400

def test_update_password_invalid_new_password(client, headers_regular_user_fixture):
    data = {
        "old_password": "mypassword",
        "new_password": "new &**password"
    }
    response = client.post('/api/users/1/update_password', json=data, headers=headers_regular_user_fixture)

    assert response.status_code == 400

    data_json = response.get_json()
    assert data_json['errors']['new_password'] == 'new_password must only contain letters, numbers and underscores.'

def test_update_password_for_admin_user(client, headers_user_admin_fixture, user_regular_fixture):
    data = {
        "old_password": "mypassword",
        "new_password": "newpassword"
    }
    response = client.post('/api/users/2/update_password', json=data, headers=headers_user_admin_fixture)

    assert response.status_code == 403