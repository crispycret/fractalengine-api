
from flask import Blueprint

mandlebrot = Blueprint('mandlebrot', __name__, url_prefix='/mandlebrot')


from . import routes, models

