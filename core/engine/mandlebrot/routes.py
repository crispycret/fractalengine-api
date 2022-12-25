
from core import db
from core.routes import response
from core.decorators import require_json, require_model_columns_in_json

from core.auth.decorators import require_login


from core.engine.mandlebrot import mandlebrot
from core.engine.mandlebrot.models import Mandlebrot #, UserMandlebrotEntry


@mandlebrot.route('/demo')
@require_model_columns_in_json(Mandlebrot)
def demo(data):
    m = Mandlebrot.create(data)
    if not m: return response(400, 'failed', data)
    from flask import request
    params = request.args()

    print (params)

    dataset = None
    if ('generate' in params):
        # generate and return a full 
        # mandlebrot dataset using the settings
        dataset = m.generate()

    data = {
        'mandlebrot': m.serialize,
        'dataset': dataset
    }
    return response(200, 'success', data)


@mandlebrot.route('/user_entry', methods=['POST'])
@require_login
@require_model_columns_in_json(Mandlebrot)
def create_user_entry(user, data):
    ''' Defines a user linked to a mandlebrot entry point (or generation settings.) '''
    m = Mandlebrot.generate(data)
    
    db.session.add(m)
    
    # entry = UserMandlebrotEntry.create(user.id, m.id)
    # db.session.ad(entry)
    # db.session.commit()

    data = {
        'mandlebrot': m.serialize,
        # 'entry': entry.serialize
    }

    return response(200, 'user_mandlebrot_entry successfully created', data)
    


