from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)



from . import routes, models

from .auth import auth
from .engine import engine

app.register_blueprint(auth)
app.register_blueprint(engine)