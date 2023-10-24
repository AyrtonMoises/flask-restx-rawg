from flask_restx import Api

from .namespaces import users_ns, games_ns, auth_ns, favorite_games_ns

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Insert your token jwt 'Bearer <your_token_jwt>'.",
    }
}

api = Api(
    version='1.0',
    title="API from RAWG",
    description='API of games from RAWG Database',
    doc='/doc',
    prefix='/api',
    authorizations=authorizations, security='jwt'
)

api.add_namespace(auth_ns)
api.add_namespace(users_ns)
api.add_namespace(games_ns)
api.add_namespace(favorite_games_ns)

