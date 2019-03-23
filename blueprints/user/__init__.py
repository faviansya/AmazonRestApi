from blueprints import db
from flask_restful import fields


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(25))
    urlimage = db.Column(db.String(1000))
    alamat = db.Column(db.String(100))
    status = db.Column(db.String(25))
    level = db.Column(db.String(25))
    transaction = db.Column(db.Integer)
    kota = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'password': fields.String,
        'username': fields.String,
        'name': fields.String,
        'urlimage': fields.String,
        'alamat': fields.String,
        'status': fields.String,
        'level': fields.String,
        'transaction': fields.Integer,
        'kota': fields.String,
    }

    def __init__(self, username, password, name, urlimage, alamat, status, level,transaction,kota):
        self.username = username
        self.password = password
        self.name = name
        self.urlimage = urlimage
        self.alamat = alamat
        self.status = status
        self.level = level
        self.transaction = transaction
        self.kota = kota

    def __repr__(self):
        return '<User %r>' % self.id

