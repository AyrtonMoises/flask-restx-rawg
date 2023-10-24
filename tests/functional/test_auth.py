def test_login_credentials(client, user_regular_fixture):
    data = {
        "username": "myusername",
        "password": "mypassword"
    }
    response = client.post('/api/auth/login', json=data)

    assert response.status_code == 200

    data_json = response.get_json()
    assert 'access_token' in data_json
    assert 'refresh_token' in data_json

def test_refresh_token(client, user_regular_fixture):
    # get credentials 
    data = {
        "username": "myusername",
        "password": "mypassword"
    }
    response = client.post('/api/auth/login', json=data)
    data_json_credentials = response.get_json()

    headers = {
        "Authorization": f"Bearer {data_json_credentials['refresh_token']}"
    }

    response = client.post('/api/auth/refresh', headers=headers)

    assert response.status_code == 200

    data_json = response.get_json()
    assert 'access_token' in data_json
