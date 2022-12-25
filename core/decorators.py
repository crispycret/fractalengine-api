

from functools import wraps
from flask import request

from core.routes import response
from core.models import required_columns

def require_json(f):
    '''' Force the request to require some form of json data to be passed. '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        try: data = request.get_json()
        except: return response(400, 'No json data provided')
        return f(data, *args, **kwargs)
    return wrapper


def require_fields_in_json(fields):
    ''' Force the request include the provided fields '''
    def func(f):
        @wraps(f)
        @require_json
        def wrapper(data, *args, **kwargs):
            for field in fields:
                if (field not in data):
                    return response(400, f'provided data is missing column `{field}')
            return f(data, *args, **kwargs)
        return wrapper
    return func


def require_model_columns_in_json(cls, ignore=['id']):
    ''' Force the request to require fields from the provided SQLAlchemy model with the option to ignore some feilds. '''
    def func(f):
        @wraps(f)
        @require_fields_in_json(required_columns(cls, ignore))
        def wrapper(data, *args, **kwargs):
            return f(data, *args, **kwargs)
        return wrapper
    return func

