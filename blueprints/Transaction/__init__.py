from blueprints import db
from flask_restful import fields


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    status = db.Column(db.String(100))
    tanggal = db.Column(db.String(100))

    response_field = {
        'id': fields.Integer,
        'item_id': fields.Integer,
        'user_id': fields.Integer,
        'owner_id': fields.Integer,
        'qty': fields.Integer,
        'status': fields.String,
        'tanggal': fields.String,

    }

    def __init__(self, item_id, user_id,owner_id, qty, status,tanggal):
        self.item_id = item_id
        self.user_id = user_id
        self.owner_id = owner_id
        self.qty = qty
        self.status = status
        self.tanggal = tanggal

    def __repr__(self):
        return '<Transaction %r>' % self.id
