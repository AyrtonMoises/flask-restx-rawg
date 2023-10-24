def test_game_search_authenticated(client, headers_regular_user_fixture):
    game_example = "The Witcher 3"
    response = client.get(
        f'/api/games/game_search/{game_example}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json[0]['id'] == 3328
    assert data_json[0]['name'] == 'The Witcher 3: Wild Hunt'
    assert data_json[0]['metacritic'] == 92
    assert data_json[0]['released'] == '2015-05-18'
    assert data_json[0]['background_image'] == 'https://media.rawg.io/media/games/618/618c2031a07bbff6b4f611f10b6bcdbc.jpg'
    assert isinstance(data_json[0]['platforms'], list)

def test_game_search_not_exists(client, headers_regular_user_fixture):
    game_example = "98ugfuijfdgjkgfnj9456f"
    response = client.get(
        f'/api/games/game_search/{game_example}',
        headers=headers_regular_user_fixture
    )
    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json == []
    
def test_game_search_without_authenticated(client):
    game_example = "The Witcher 3"
    response = client.get(
        f'/api/games/game_search/{game_example}'
    )

    assert response.status_code == 401

def test_game_details_authenticated(client, headers_regular_user_fixture):
    game_id_example = 324997
    response = client.get(
        f'/api/games/game_details/{game_id_example}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 200

    data_json = response.get_json()
    assert data_json['id'] == 324997
    assert data_json['name'] == "Baldur's Gate III"
    assert isinstance(data_json['metacritic'], int) or data_json['metacritic'] is None
    assert data_json['released'] == '2023-08-03'
    assert isinstance(data_json['background_image'], str) or data_json['background_image'] is None
    assert isinstance(data_json['platforms'], list)
    assert isinstance(data_json["screenshots"], list)

def test_game_details_without_authenticated(client):
    game_id_example = 324997
    response = client.get(
        f'/api/games/game_details/{game_id_example}'
    )

    assert response.status_code == 401

def test_game_details_not_found(client, headers_regular_user_fixture):
    game_id_example = 9049058434454555555555555
    response = client.get(
        f'/api/games/game_details/{game_id_example}',
        headers=headers_regular_user_fixture
    )

    assert response.status_code == 404

    data_json = response.get_json()
    assert data_json["message"] == "Game not found"

def test_games_most_popular_year_authenticated(client, headers_regular_user_fixture):
    response = client.get(
        f'/api/games/games_most_popular_year',
        headers=headers_regular_user_fixture
    )
    assert response.status_code == 200

    data_json = response.get_json()
    for item in data_json:
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
        assert isinstance(item['metacritic'], int) or item['metacritic'] is None
        assert isinstance(item['released'], str)
        assert isinstance(item['background_image'], str) or item['background_image'] is None
        assert isinstance(item['platforms'], list)

def test_games_most_popular_year_authenticated(client, headers_regular_user_fixture):
    response = client.get(
        '/api/games/games_most_popular_year',
        headers=headers_regular_user_fixture
    )
    assert response.status_code == 200

    data_json = response.get_json()
    
    for item in data_json:
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
        assert isinstance(item['metacritic'], int) or item['metacritic'] is None
        assert isinstance(item['released'], str)
        assert isinstance(item['background_image'], str) or item['background_image'] is None
        assert isinstance(item['platforms'], list)

def test_games_most_popular_year_without_authenticated(client):
    response = client.get('/api/games/games_most_popular_year')
    assert response.status_code == 401

def test_games_most_awaited_year_authenticated(client, headers_regular_user_fixture):
    response = client.get(
        '/api/games/games_most_awaited_year',
        headers=headers_regular_user_fixture
    )
    assert response.status_code == 200

    data_json = response.get_json()
    assert isinstance(data_json, list)
    assert isinstance(data_json[0]['id'], int)
    assert isinstance(data_json[0]['name'], str)
    assert isinstance(data_json[0]['metacritic'], int) or data_json[0]['metacritic'] is None
    assert isinstance(data_json[0]['released'], str) or data_json[0]['released'] is None
    assert isinstance(data_json[0]['background_image'], str) or data_json[0]['background_image'] is None
    assert isinstance(data_json[0]['platforms'], list)

def test_games_most_awaited_year_without_authenticated(client):
    response = client.get('/api/games/games_most_awaited_year')
    assert response.status_code == 401

def test_games_most_popular_last_30_days_authenticated(client, headers_regular_user_fixture):
    response = client.get(
        '/api/games/released_most_popular_last_30_days',
        headers=headers_regular_user_fixture
    )
    assert response.status_code == 200

    data_json = response.get_json()
    for _, games in data_json.items():
        for game in games:
            assert isinstance(game['id'], int)
            assert isinstance(game['name'], str)
            assert isinstance(game['metacritic'], int) or game['metacritic'] is None
            assert isinstance(game['released'], str) or game['released'] is None
            assert isinstance(game['background_image'], str) or game['background_image'] is None

def test_games_most_popular_last_30_days_without_authenticated(client):
    response = client.get('/api/games/released_most_popular_last_30_days')
    assert response.status_code == 401
