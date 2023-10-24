from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request


def admin_required():
    """ access only admin users """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('is_admin', False):
                return fn(*args, **kwargs)
            else:
                return {'message': 'only admin users!'}, 403

        return decorator

    return wrapper

def current_user_or_admin_required():
    """ access only current user """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('sub', False) == kwargs['user_id'] or claims.get('is_admin', False):
                return fn(*args, **kwargs)
            else:
                return {'message': 'only the user or admins can access/change his information'}, 403

        return decorator

    return wrapper

def current_user_required():
    """ access only current user """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('sub', False) == kwargs['user_id']:
                return fn(*args, **kwargs)
            else:
                return {'message': 'only the user can access/change his information'}, 403

        return decorator

    return wrapper