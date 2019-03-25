from blueprints import db
from flask_restful import fields


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.String(500))
    item_gambar = db.Column(db.String(500))
    item_harga = db.Column(db.String(500))

    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(500))
    user_alamat = db.Column(db.String(500))
    user_gambar = db.Column(db.String(500))

    owner_id = db.Column(db.Integer)
    owner_name = db.Column(db.String(500))
    owner_alamat = db.Column(db.String(500))
    owner_gambar = db.Column(db.String(500))

    qty = db.Column(db.Integer)
    status = db.Column(db.String(100))
    tanggal = db.Column(db.String(100))
    deliver = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'item_id': fields.Integer,
        'item_name': fields.String,
        'item_gambar': fields.String,
        'item_harga': fields.String,

        'user_id': fields.Integer,
        'user_name': fields.String,
        'user_alamat': fields.String,
        'user_gambar': fields.String,

        'owner_id': fields.Integer,
        'owner_name': fields.String,
        'owner_alamat': fields.String,
        'owner_gambar': fields.String,

        'qty': fields.Integer,
        'status': fields.String,
        'tanggal': fields.String,
        'deliver': fields.String,

    }

    def __init__(self, item_id, item_name, item_gambar, item_harga, user_id, user_name, user_alamat, user_gambar, owner_id, owner_name, owner_alamat, owner_gambar, qty, status, tanggal, deliver):
        self.item_id = item_id
        self.item_name = item_name
        self.item_gambar = item_gambar
        self.item_harga = item_harga

        self.user_id = user_id
        self.user_name = user_name
        self.user_alamat = user_alamat
        self.user_gambar = user_gambar

        self.owner_id = owner_id
        self.owner_name = owner_name
        self.owner_alamat = owner_alamat
        self.owner_gambar = owner_gambar

        self.qty = qty
        self.status = status
        self.tanggal = tanggal
        self.deliver = deliver

    def __repr__(self):
        return '<Transaction %r>' % self.id
