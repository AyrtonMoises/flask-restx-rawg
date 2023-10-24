from marshmallow import fields, validate, validates_schema, ValidationError, validates, pre_load, Schema

from app.extensions import ma
from app.api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    username = fields.String(
        allow_none=True,
        validate=[
            validate.Length(min=3),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error="username must only contain letters, numbers and underscores."),
        ],
        error_messages={"required": "Field 'username' is required."},
    )
    email = fields.String(
        allow_none=True,
        validate=validate.Email(),
        error_messages={"required": "Field 'email' is required."}
    )

    password = fields.String(
        allow_none=True,
        validate=[
            validate.Length(min=3),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error="password must only contain letters, numbers and underscores."),
        ],
        error_messages={"required": "Field 'password' is required."},
    )

    def transform_to_lower(self, data, field_name):
        if field_name in data:
            data[field_name] = data[field_name].lower()
        return data

    @pre_load
    def transform_fields(self, data, **kwargs):
        self.transform_to_lower(data, "username")
        self.transform_to_lower(data, "email")
        return data

    @validates("username")
    def validate_username(self, username):
        user_id = self.context.get('user_id')
        if username:
            query = UserModel.query.filter(UserModel.username == username)
            if user_id:
                query = query.filter(UserModel.id != user_id)
            if query.first():
                raise ValidationError('this username already exists')

    @validates("email")
    def validate_email(self, email):
        user_id = self.context.get('user_id')
        if email:
            query = UserModel.query.filter(UserModel.email == email)
            if user_id:
                query = query.filter(UserModel.id != user_id)
            if query.first():
                raise ValidationError('this email already exists')

    class Meta:
        model = UserModel
        load_instance = True


class UserUpdatePasswordSchema(Schema):

    old_password = fields.String(
        error_messages={"required": "Field 'old_password' is required."},
    )

    new_password = fields.String(
        validate=[
            validate.Length(min=3),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error="new_password must only contain letters, numbers and underscores."),
        ],
        error_messages={"required": "Field 'new_password' is required."},
    )