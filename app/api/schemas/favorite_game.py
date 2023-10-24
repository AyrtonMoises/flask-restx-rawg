from marshmallow import fields, validates, ValidationError

from app.extensions import ma
from app.api.models.favorite_game import FavoriteGameModel

class FavoriteGameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteGameModel
        load_instance = True
        include_relationships = True

    @validates("game_rawg_id")
    def validate_game_rawg_id(self, game_rawg_id):
        user_id = self.context.get('user_id')
        result = FavoriteGameModel.query.filter_by(game_rawg_id=game_rawg_id,user_id=user_id).first()
        if result:
            raise ValidationError('this game RAWG already exists in your user')