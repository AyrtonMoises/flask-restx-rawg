from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

from app.api.models.user import UserModel


auth_ns = Namespace('auth', description='Auth operations')

item = auth_ns.model('login', {
    'username': fields.String(description='username'),
    'password': fields.String(description='user password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc(security=None)
    @auth_ns.expect(item)
    def post(self):
        data = auth_ns.payload
        username = data['username']
        password = data['password']
        user = UserModel.get_user_by_username(username)
        if user:
            if user.verify_password(password, user.password):
                access_token = create_access_token(
                    identity=user.id, additional_claims={"is_admin": user.is_admin}
                )
                refresh_token = create_refresh_token(identity=user.id)
                return {'access_token': access_token, 'refresh_token': refresh_token}
        return {'message': 'Invalid credentials'}, 401


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
