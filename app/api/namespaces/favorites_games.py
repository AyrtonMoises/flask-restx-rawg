from flask_restx import Resource, fields, Namespace
from marshmallow import ValidationError

from app.api.utils.wrappers_auth import current_user_required
from app.api.models.favorite_game import FavoriteGameModel
from app.api.schemas.favorite_game import FavoriteGameSchema
from app.api.models.user import UserModel
from app.services.api_rawg import ApiRAWG


favorite_games_ns = Namespace('favorite_games', description='Favorite games operations')

favorite_game_schema = FavoriteGameSchema()
favorite_game_list_schema = FavoriteGameSchema(many=True)

ITEM_NOT_FOUND = 'Favorite game not found'
USER_NOT_FOUND = 'User not found'

item = favorite_games_ns.model('favorite_game', {
    'game_rawg_id': fields.Integer(description='id game in RAWG database')
})

@favorite_games_ns.route('/<int:user_id>/<int:game_id>')
@favorite_games_ns.response(404, ITEM_NOT_FOUND)
class FavoriteGame(Resource):
    
    @current_user_required()
    @favorite_games_ns.doc('get_favorite_game')
    def get(self, user_id, game_id):
        '''Get favorite game'''
        game = FavoriteGameModel.get_favorite_game_by_id(game_id)
        if game:
            return favorite_game_schema.dump(game)
        return {'message': ITEM_NOT_FOUND}, 404

    @current_user_required()
    @favorite_games_ns.doc('delete_favorite_game')
    @favorite_games_ns.response(204, 'favorite game deleted')
    @favorite_games_ns.response(404, ITEM_NOT_FOUND)
    def delete(self, user_id, game_id):
        '''Delete favorite game'''
        game = FavoriteGameModel.get_favorite_game_by_id(game_id)
        if game:
            FavoriteGameModel.delete_favorite_game(game)
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404


@favorite_games_ns.route('/<int:user_id>')
class FavoriteGamesList(Resource):
    @current_user_required()
    @favorite_games_ns.doc('list_favorite_games')
    def get(self, user_id):
        '''List all favorites games by user id'''
        all_favorites_games = FavoriteGameModel.get_all_favorite_games_by_user_id(user_id)
        return favorite_game_list_schema.dump(all_favorites_games), 200

    @current_user_required()
    @favorite_games_ns.doc('create_favorite_game')
    @favorite_games_ns.expect(item)
    @favorite_games_ns.response(201, 'favorite game created')
    def post(self, user_id):
        '''Create a favorite game'''
        data = favorite_games_ns.payload
        # validate game id exists in RAWG API
        data_rawg = ApiRAWG().game_details(data['game_rawg_id']) 

        if not data_rawg:
            return {"message": "Game ID in RAWG not found"}, 400
           
        user = UserModel.get_user_by_id(user_id)
        if user:
            favorite_game_schema.context = {'user_id': user_id}
            errors = favorite_game_schema.validate(data)
            if errors:
                raise ValidationError(errors)

            game = FavoriteGameModel.create_favorite_game(data, user_id)
            game_serialized = favorite_game_schema.dump(game)
            return game_serialized, 201
        return {"message": USER_NOT_FOUND}, 404
