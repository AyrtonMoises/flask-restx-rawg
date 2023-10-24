from datetime import datetime

from app.api.models.favorite_game import FavoriteGameModel 


def test_create_favorite_game(client):
    data = {
        'game_rawg_id': 3328
    }
    favorite_game = FavoriteGameModel.create_favorite_game(data, 1)

    assert favorite_game.id == 1
    assert favorite_game.game_rawg_id == 3328
    assert favorite_game.user_id == 1
    assert isinstance(favorite_game.created_at, datetime)

def test_get_favorite_game_by_id(client, favorite_games_fixture):
    favorite_game = FavoriteGameModel.get_favorite_game_by_id(1)
    assert favorite_game.id == 1
    assert favorite_game.game_rawg_id == 3328
    assert favorite_game.user_id == 1
    assert isinstance(favorite_game.created_at, datetime)

def test_get_all_favorite_games_by_user_id(client, favorite_games_fixture):
    favorite_game_list = FavoriteGameModel.get_all_favorite_games_by_user_id(1)
    assert len(favorite_game_list) == 2

def test_delete_favorite_game(client, favorite_games_fixture):
    favorite_game = FavoriteGameModel.get_favorite_game_by_id(1)
    FavoriteGameModel.delete_favorite_game(favorite_game)
    favorite_game_delete = FavoriteGameModel.get_favorite_game_by_id(1)
    assert favorite_game_delete is None