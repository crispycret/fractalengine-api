import jwt
import uuid
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from core import db
from core import Configuration


def utcfuture(weeks=0, days=0, hours=8, minutes=0, seconds=0):
    datetime.timedelta()
    return datetime.datetime.utcnow() + datetime.timedelta(
        weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds
    )


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires = db.Column(db.DateTime, default=utcfuture)

    def encode(self, key=Configuration.SECRET_KEY):
        data = self.serialize
        del data['id']
        return jwt.encode(data, key, 'HS256')
        

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created': self.created.isoformat(),
            'expires': self.expires.isoformat(),
        }

    @staticmethod
    def decode(token, key=Configuration.SECRET_KEY):
        try: return jwt.decode(token, key, 'HS256')
        except: return None













class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    public_id = db.Column(db.String(96), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    tokens = db.relationship('Token', backref='user', lazy=True, cascade='all, delete-orphan')


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_token(self, expires=utcfuture()):
        token = Token(user_id=self.id, expires=expires)
        db.session.add(token)
        db.session.commit()
        return token

    def purge_tokens(self):
        try:
            tokens = Token.query.filter_by(user_id=self.id).all()
            [db.session.delete(token) for token in tokens]
            db.session.commit()
            return True
        except: return False

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'public_id': self.public_id,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
        }

    @property
    def full_serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password,
            'public_id': self.public_id,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
        }


    @staticmethod
    def create(username, email, password):
        public_id = username + '#' + str(uuid.uuid4()).split('-')[-1]
        password_hash = generate_password_hash(password)
        payload = { 'username':username, 'email':email, 'password':password_hash, 'public_id':public_id}
        return User(**payload)

    @staticmethod
    def exists(email):
        ''' Return true or false for if a user with the provided email is found in the database. '''
        user = User.query.filter_by(email=email).first()
        if not user: return False
        return user

    @staticmethod
    def from_token(token, encoded=True, decode_key=Configuration.SECRET_KEY):
        ''' provided a token (encoded or decoded) return the corresponding user. '''
        if (encoded or type(token) == str):
            token = Token.decode(token, decode_key)
        if (type(token) is not dict): return None # Must be a dict
        user = User.query.filter_by(id=token['user_id']).first()
        return user
