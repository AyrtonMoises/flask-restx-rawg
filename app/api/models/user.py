from passlib.apps import custom_app_context as pwd_context

from app.extensions import db
from .favorite_game import FavoriteGameModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    favorite_games = db.relationship(
        "FavoriteGameModel",
        backref="user",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password, hash_password):
        return pwd_context.verify(password, hash_password)

    @classmethod
    def get_user_by_id(cls, user_id):
        user = cls.query.filter_by(id=user_id).first()
        return user

    @classmethod
    def get_user_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

    @classmethod
    def get_all_users(cls):
        users = cls.query.all()
        return users

    @classmethod
    def create_user(cls, data):
        password_hash = cls.hash_password(data['password'])
        user = cls(
            username=data['username'],
            password=password_hash,
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def update_user(cls, user_id, data):
        user = cls.get_user_by_id(user_id)
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        db.session.commit()
        return user

    @classmethod
    def update_password(cls, user_id, new_password):
        user = cls.get_user_by_id(user_id)
        new_password_hash = cls.hash_password(new_password)
        user.password = new_password_hash
        db.session.commit()
        return user

    @classmethod
    def delete_user(cls, user):
        db.session.delete(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username