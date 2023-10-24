from flask_restx import Resource, fields, Namespace
from marshmallow import ValidationError

from app.api.models.user import UserModel
from app.api.schemas.user import UserSchema, UserUpdatePasswordSchema
from app.api.utils.wrappers_auth import admin_required, current_user_or_admin_required, current_user_required


users_ns = Namespace('users', description='Users related operations')

user_schema = UserSchema()
user_put_schema = UserSchema(only=('username','email'))
user_output_schema = UserSchema(exclude=('password',))
user_list_schema = UserSchema(many=True, exclude=('password',))
user_update_password_schema = UserUpdatePasswordSchema()


ITEM_NOT_FOUND = 'User not found'

item = users_ns.model('user', {
    'username': fields.String(description='username'),
    'password': fields.String(description='user password'),
    'email': fields.String(description='user email')
})

item_update = users_ns.model('user_update', {
    'username': fields.String(description='username'),
    'email': fields.String(description='user email')
})

item_password = users_ns.model('user_password', {
    'old_password': fields.String(description='old password'),
    'new_password': fields.String(description='new password')
})

@users_ns.route('/<int:user_id>')
@users_ns.response(404, 'user not found')
@users_ns.param('user_id', 'The user identifier')
class User(Resource):
    
    @current_user_or_admin_required()
    @users_ns.doc('get_user')
    @users_ns.expect(item)
    def get(self, user_id):
        '''Get user'''
        user_data = UserModel.get_user_by_id(user_id)
        if user_data:
            return user_output_schema.dump(user_data)
        return {'message': ITEM_NOT_FOUND}, 404

    @users_ns.doc('update_user')
    @current_user_or_admin_required()
    @users_ns.expect(item_update)
    def put(self, user_id):
        '''Update user'''
        data_user = UserModel.get_user_by_id(user_id)
        if data_user:
            data = users_ns.payload
            # passes id to context to validate user data
            user_put_schema.context = {'user_id': user_id}
            errors = user_put_schema.validate(data)
            if errors:
                raise ValidationError(errors)
            user = UserModel.update_user(user_id, data)
            user_serialized = user_output_schema.dump(user)
            return user_serialized, 200
        return {'message': ITEM_NOT_FOUND}, 404

    @current_user_or_admin_required()
    @users_ns.doc('delete_user')
    @users_ns.response(204, 'user deleted')
    @users_ns.response(404, 'user not found')
    def delete(self, user_id):
        '''Delete user'''
        user_data = UserModel.get_user_by_id(user_id)
        if user_data:
            UserModel.delete_user(user_data)
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404


@users_ns.route('/')
class UserList(Resource):
    @admin_required()
    @users_ns.doc('list_users')
    def get(self):
        '''List all users'''
        all_users = UserModel.get_all_users()
        return user_list_schema.dump(all_users), 200

    @users_ns.doc(security=None)
    @users_ns.doc('create_user')
    @users_ns.expect(item)
    @users_ns.response(201, 'user created')
    def post(self):
        '''Create a user'''
        data = users_ns.payload
        errors = user_schema.validate(data)
        if errors:
           raise ValidationError(errors)

        user_data = UserModel.create_user(data)
        user_serialized = user_output_schema.dump(user_data)
        return user_serialized, 201

@users_ns.route('/<int:user_id>/update_password')
@users_ns.response(404, 'user not found')
@users_ns.response(400, 'password is incorrect')
@users_ns.param('user_id', 'The user identifier')
class UpdatePasswordUser(Resource):

    @current_user_required()
    @users_ns.doc('password_user')
    @users_ns.expect(item_password)
    def post(self, user_id):
        '''Update password user'''
        data = users_ns.payload
        user = UserModel.get_user_by_id(user_id)
        if user:
            errors = user_update_password_schema.validate(data)
            if errors:
                raise ValidationError(errors)
            if user.verify_password(data['old_password'], user.password):
                UserModel.update_password(user_id, data['new_password'])
                return {"message": "password updated"}, 200
            else:
                return {'message': 'password is incorrect'}, 400
        return {'message': ITEM_NOT_FOUND}, 404

