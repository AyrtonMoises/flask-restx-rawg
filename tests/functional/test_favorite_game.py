from datetime import datetime


def test_favorite_game_current_user(client, headers_regular_user_fixture, favorite_games_fixture):
    game_rawg_id = 339958
    user_id = 1
    favorite_id = 1

    response = client.get(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['id'] == 1
    assert data_json['game_rawg_id'] == 3328
    assert data_json['user'] == 1
    assert isinstance(
        datetime.strptime(
            data_json['created_at'],'%Y-%m-%dT%H:%M:%S.%f'
        ), datetime)

def test_favorite_game_another_user(
    client, headers_user_admin_fixture,
    user_regular_fixture, favorite_games_fixture
    ):
    user_id = 2
    favorite_id = 1

    response = client.get(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_user_admin_fixture
    )
    assert response.status_code == 403

def test_favorite_game_not_authenticated(client):
    user_id = 2
    favorite_id = 1

    response = client.get(
        f'/api/favorite_games/{user_id}/{favorite_id}'
    )
    assert response.status_code == 401

def test_favorite_game_not_found(client, headers_regular_user_fixture, favorite_games_fixture):
    user_id = 1
    favorite_id = 999

    response = client.get(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 404

def test_create_favorite_games_current_user(client, headers_regular_user_fixture):
    data = {"game_rawg_id": 339958}
    user_id = 1

    response = client.post(
        f'/api/favorite_games/{user_id}', json=data, headers=headers_regular_user_fixture
    )

    assert response.status_code == 201

    data_json = response.get_json()

    assert data_json['id'] == 1
    assert data_json['game_rawg_id'] == 339958
    assert isinstance(
        datetime.strptime(
            data_json['created_at'],'%Y-%m-%dT%H:%M:%S.%f'
        ), datetime)
    assert data_json['user'] == 1

def test_create_favorite_games_when_game_rawg_not_finded(client, headers_regular_user_fixture):
    data = {"game_rawg_id": 99999999999999999999999}
    user_id = 1

    response = client.post(
        f'/api/favorite_games/{user_id}', json=data, headers=headers_regular_user_fixture
    )
    assert response.status_code == 400

def test_create_favorite_games_with_another_user(
        client, headers_user_admin_fixture, headers_regular_user_fixture
    ):
    data = {"game_rawg_id": 339958}
    user_id = 2

    response = client.post(
        f'/api/favorite_games/{user_id}', json=data, headers=headers_user_admin_fixture
    )

    assert response.status_code == 403

def test_create_favorite_game_without_credentials(client):
    data = {"game_rawg_id": 339958}
    user_id = 2

    response = client.post(
        f'/api/favorite_games/{user_id}', json=data
    )

    assert response.status_code == 401

def test_delete_favorite_game_current_user(
        client, headers_regular_user_fixture, favorite_games_fixture
    ):
    user_id = 1
    favorite_id = 1

    response = client.delete(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 204

def test_delete_favorite_game_another_user(
        client, headers_user_admin_fixture, favorite_games_fixture,
        user_regular_fixture
    ):
    user_id = 2
    favorite_id = 1

    response = client.delete(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_user_admin_fixture
    )

    assert response.status_code == 403

def test_delete_favorite_game_not_found(
        client, headers_user_admin_fixture, favorite_games_fixture,
    ):
    user_id = 1
    favorite_id = 999

    response = client.delete(
        f'/api/favorite_games/{user_id}/{favorite_id}',
        headers=headers_user_admin_fixture
    )

    assert response.status_code == 404

def test_favorite_games_current_user(
        client, headers_regular_user_fixture, favorite_games_fixture
    ):
    user_id = 1
    favorite_games_list = [
        {"game_rawg_id": 3328}, {"game_rawg_id": 339958}
    ] 

    response = client.get(
        f'/api/favorite_games/{user_id}',
        headers=headers_regular_user_fixture
    )

    data_json = response.get_json()

    assert len(data_json) == 2

    for index, item in enumerate(favorite_games_list):
        assert isinstance(data_json[index]['id'], int)
        assert data_json[index]['game_rawg_id'] == item['game_rawg_id']
        assert isinstance(
            datetime.strptime(
                data_json[index]['created_at'],'%Y-%m-%dT%H:%M:%S.%f'
            ), datetime)
        assert data_json[index]['user'] == 1

def test_favorite_games_another_user(
        client, headers_user_admin_fixture, user_regular_fixture, favorite_games_fixture
    ):
    user_id = 2
    response = client.get(
        f'/api/favorite_games/{user_id}',
        headers=headers_user_admin_fixture
    )
    assert response.status_code == 403
    
def test_favorite_games_without_credentials(client):
    user_id = 2
    response = client.get(f'/api/favorite_games/{user_id}')

    assert response.status_code == 401