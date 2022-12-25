import os
from dotenv import load_dotenv


load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__name__))

DATABASE_URI = os.environ.get("DATABASE_URI") or \
    'sqlite:///' + os.path.join(BASEDIR, 'default.db')


class Configuration(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", 'TESTING_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI


    