from datetime import datetime

from app.extensions import db


class FavoriteGameModel(db.Model):
    __tablename__ = "favorite_games"

    id = db.Column(db.Integer, primary_key=True)
    game_rawg_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def get_favorite_game_by_id(cls, favorite_id):
        favorite = cls.query.filter_by(id=favorite_id).first()
        return favorite

    @classmethod
    def get_all_favorite_games_by_user_id(cls, user_id):
        favorite_games = cls.query.filter_by(user_id=user_id).all()
        return favorite_games

    @classmethod
    def create_favorite_game(cls, data, user_id):
        favorite = cls(
            game_rawg_id=data['game_rawg_id'],
            user_id=user_id
        )
        db.session.add(favorite)
        db.session.commit()
        return favorite

    @classmethod
    def delete_favorite_game(cls, favorite_game):
        db.session.delete(favorite_game)
        db.session.commit()

    def __repr__(self):
        return '<Favorite game #%r>' % self.id