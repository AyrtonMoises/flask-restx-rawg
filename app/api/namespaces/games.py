from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from app.services.api_rawg import ApiRAWG
from app.extensions import cache


games_ns = Namespace('games', description='Data from games')

api_rawg = ApiRAWG()

ITEM_NOT_FOUND = 'Game not found'

@games_ns.route('/game_search/<string:game_name>')
class GameSearch(Resource):
    @jwt_required()
    def get(self, game_name):
        '''Get search by name game'''
        data = api_rawg.game_search(game_name)
        return data

@games_ns.route('/game_details/<int:id_game>')
class GameDetails(Resource):
    @jwt_required()
    def get(self, id_game):
        '''Get details from game'''
        data = api_rawg.game_details(id_game)
        if data:
            screenshots = api_rawg.game_screenshots(id_game)
            data.update({'screenshots': screenshots})
            return data
        return {'message': ITEM_NOT_FOUND}, 404

@games_ns.route('/games_most_popular_year')
class GamesMostPopularYear(Resource):
    @jwt_required()
    @cache.cached(timeout=3600)
    def get(self):
        '''Get games most popular since year'''
        data = api_rawg.games_most_popular_by_current_year()
        return data

@games_ns.route('/games_most_awaited_year')
class GamesMostAwaitedYear(Resource):
    @jwt_required()
    @cache.cached(timeout=3600)
    def get(self):
        '''Get games most awaited since year'''
        data = api_rawg.games_most_awaited_by_current_year()
        return data


@games_ns.route('/released_most_popular_last_30_days')
class GameReleasedLast30days(Resource):
    @jwt_required()
    @cache.cached(timeout=3600)
    def get(self):
        '''Get games most popular released in the last 30 days'''
        data = api_rawg.games_most_popular_released_last_30_days()
        return data

