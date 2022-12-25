from functools import wraps
from flask import request


from core.routes import response
from core.auth.models import User


def require_login(f):
    ''' Require request to include a valid Authentication token. Return corresponding user. '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        if ('Authorization' not in request.headers):
            return response(401, 'Authentication token was not provided.')
        token = request.headers['Authorization']
        user = User.from_token(token)
        if (not user): 
            return response(401, 'Could not find user from provided token.')
        return f(user, *args, **kwargs)
    return wrapper


