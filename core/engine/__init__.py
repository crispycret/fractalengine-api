from flask import Blueprint


engine = Blueprint('engine', __name__, url_prefix='/engine')


from core.engine.mandlebrot import mandlebrot
engine.register_blueprint(mandlebrot)

from . import routes, models