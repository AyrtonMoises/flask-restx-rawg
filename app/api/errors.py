from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import requests


def configure_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """ Get validation errors """
        error_messages = {}
        for field, messages in error.messages.items():
            for message in messages:
                error_messages.update({field: message})
        return {'message': 'Validation error', 'errors': error_messages}, 400
 
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """ Get Database errors """
        return {'message': 'Database error'}, 500

    @app.errorhandler(Exception)
    def handle_server_error(error):
        """ Get Internal server errors """
        return {'message': 'Internal server error'}, 500
        
    @app.errorhandler(requests.exceptions.RequestException)
    def handle_request_error(error):
        """ Get API external errors """
        # if status is 404
        if error.response.status_code == 404:
            return {'message': 'Not found data in RAWG'}, 404
        else:
            return {'message': 'Error API RAWG'}, 403