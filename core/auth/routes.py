import math
from flask import request
from flask import current_app as app

from core import db
from core.routes import response
from core.models import required_columns
from core.decorators import require_json, require_fields_in_json, require_model_columns_in_json

from core.auth import auth
from core.auth.models import User
from core.auth.decorators import require_login


@auth.route('/register', methods=['POST'])
# @require_model_columns_in_json(User, ignore=['id', 'public_id'])
@require_fields_in_json(['username', 'email', 'password'])
def register(data):
    ''' Provided the request includes the nesseccary json fields create a user. '''
    if User.exists(data['email']):
        return response(409, f'user with email {data["email"]} already exitsts')

    try: user = User.create(data['username'], data['email'], data['password'])
    except Exception as e: return response(400, 'Failed to create user', str(e))

    try:
        db.session.add(user)
        db.session.commit()
    except: return response(400, 'Failed to save user to the database')

    return response(200, f'user {data["username"]} created.', user.serialize)




@auth.route('/login', methods=['POST'])
@require_fields_in_json(['email', 'password'])
def login(data): 
    ''' Provided the request includes the nesseccary valid json fields create a token for the user. '''
    user = User.exists(data['email'])
    if not user:
        return response(400, f'No account with email {data["email"]} exists')

    if (not user.check_password(data['password'])):
        return response(401, f'incorrect password provided')

    data = {
        'user': user.serialize,
        'Authorization': user.create_token().encode()
    }
    return response(200, 'login success', data)


@auth.route('/delete_account', methods=['POST'])
# @require_token
def delete_account(): pass






''' 
When stacking decorators it is important to note the order of the routes paramters.
The first decorator used will have it's returning data field in the last positional argument.

@require_login -> user
@require_json -> data
def test(data, user): pass

@require_json -> data
@require_login -> user
def test(user, data): pass
'''


@auth.route('/test_token')
@require_login
def test_token(user):
    return response(200, 'Token is working. User found', user.serialize)
    



@auth.route('/test_token_w_json')
@require_login
@require_json
def test_token_w_json(data, user):
    return response(200, 'Token is working. User found', {'user':user.serialize, 'extra': data})
    


@auth.route('/users', methods=['GET'], defaults={'page':1, 'per_page':25})
@auth.route('/users/<int:page>', methods=['GET'], defaults={'per_page':25})
def get_users(page, per_page):
    ''' 
    Return a page of paginated users
    Use optional parameters to define the scope of the request.
    '''
    max_per_page = 50
    per_page = per_page if (per_page <= max_per_page) else max_per_page 
    
    users = User.query.paginate(
        page=page, 
        per_page=app.config.get('USERS_PER_PAGE', max_per_page), 
        error_out=False
    )
    users = [user.serialize for user in users.items]
    return response(200, 'success', {'users': users})









