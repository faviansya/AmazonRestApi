from blueprints import db
from flask_restful import fields


class Cart(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itemname = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    tanggal_upload = db.Column(db.String(1000))
    berat = db.Column(db.Integer)
    urlimage = db.Column(db.String(500))
    qty = db.Column(db.Integer)
    status = db.Column(db.String(500))

    response_field = {
        'id': fields.Integer,
        'itemname': fields.String,
        'harga': fields.Integer,
        'user_id': fields.Integer,
        'item_id': fields.Integer,
        'tanggal_upload': fields.String,
        'berat': fields.Integer,
        'urlimage': fields.String,
        'qty': fields.Integer,
        'status': fields.String,

    }

    def __init__(self, itemname, harga, user_id, item_id, tanggal_upload,berat,urlimage,qty,status):
        self.itemname = itemname
        self.harga = harga
        self.user_id = user_id
        self.item_id = item_id
        self.tanggal_upload = tanggal_upload
        self.berat = berat
        self.urlimage = urlimage
        self.qty = qty
        self.status = status

    def __repr__(self):
        return '<Cart %r>' % self.id
