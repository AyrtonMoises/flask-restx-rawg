import pytest

from app import create_app
from app.extensions import db
from app.api.models.user import UserModel
from app.api.models.favorite_game import FavoriteGameModel


@pytest.fixture(scope="function")
def app():
    app = create_app('config.ConfigTest')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def user_regular_fixture(app):
    data = {
        'username': 'myusername',
        'password': 'mypassword',
        'email': 'user@test.com'
    }
    user = UserModel.create_user(data)
    return user

@pytest.fixture(scope="function")
def user_admin_fixture(app):
    data = {
        'username': 'user_admin',
        'password': 'admin_password',
        'email': 'admin@test.com'
    }
    user = UserModel.create_user(data)
    user.is_admin = True
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def favorite_games_fixture(app):
    data = [
        FavoriteGameModel(game_rawg_id=3328, user_id=1),
        FavoriteGameModel(game_rawg_id=339958, user_id=1),
        FavoriteGameModel(game_rawg_id=3328, user_id=2),

    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return FavoriteGameModel.query.all()

@pytest.fixture(scope="function")
def headers_regular_user_fixture(client, user_regular_fixture):
    data = {
        "username": "myusername",
        "password": "mypassword"
    }
    response = client.post('/api/auth/login', json=data)
    data_json = response.get_json()
    return {
        "Authorization": f"Bearer {data_json['access_token']}"
    }

@pytest.fixture(scope="function")
def headers_user_admin_fixture(client, user_admin_fixture):
    data = {
        "username": "user_admin",
        "password": "admin_password"
    }
    response = client.post('/api/auth/login', json=data)
    data_json = response.get_json()
    return {
        "Authorization": f"Bearer {data_json['access_token']}"
    }

