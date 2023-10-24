import click
from flask.cli import with_appcontext

from app.api.models.user import UserModel
from app.extensions import db
from app.api.schemas.user import UserSchema 


@click.command("create-user-admin")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@with_appcontext
def create_user_admin(username, password, email):
    data = {
        "username": username,
        "password": password,
        "email": email
    }
    errors = UserSchema().validate(data)
    if errors:
        raise ValueError(errors)

    user = UserModel.create_user(data)
    user.is_admin = True
    db.session.commit()
    click.echo("User admin created")

def init_app(app):
    app.cli.add_command(create_user_admin)