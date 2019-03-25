import json
import logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.user import *
from . import *
from ..user import *
from ..item import *
from ..cart import *
import datetime


bp_transaction = Blueprint('transaction', __name__)
api = Api(bp_transaction)


class TransactionResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self,transaction_id = None):
        jwtclaim = get_jwt_claims()

        parser = reqparse.RequestParser()
        parser.add_argument('transaction_id', type=int, location='args')
        args = parser.parse_args()

        if(transaction_id == "seller"):
            qry_seller = Transaction.query.filter(Transaction.owner_id.like(jwtclaim['id'])).all()
            return {'status' : 'Success',  'Data' : marshal(qry_seller, Transaction.response_field)}, 200, {'Content_type' : 'application/json'}

        if(transaction_id == "confirm"):
            qry_seller = Transaction.query.get(args["transaction_id"])
            qry_seller.deliver = "delivered"
            db.session.commit()
            return {'status' : 'Success',  'Data' : marshal(qry_seller, Transaction.response_field)}, 200, {'Content_type' : 'application/json'}


        qry_transaction = Transaction.query.filter(Transaction.user_id.like(jwtclaim['id'])).all()
        # transaction_marshal = marshal(qry_transaction, Transaction.response_field)
        # qry_getdata= Transaction.query

        # qry_item = Item.query.get(transaction_marshal['item_id'])
        # item_marshal = marshal(qry_item, Item.response_field)

        # qry_user = User.query.get(transaction_marshal['user_id'])
        # user_marshal = marshal(qry_user, User.response_field)

        # rows = []
        # for row in qry_transaction:
        #     rows.append(marshal(row, Transaction.response_field))

        
        # Transaction_row = []
        # for row in user_qry.limit(args['rp']).offset(offside).all():
        #     user_row.append(marshal(row, User.response_field))

        return {'status' : 'Success',  'Data' : marshal(qry_transaction, Transaction.response_field)}, 200, {'Content_type' : 'application/json'}


    def post(self):
        currentDT = datetime.datetime.now()

        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', type=int, location='args')
        args = parser.parse_args()

        qry_cart = Cart.query.get(args['cart_id'])
        cart_marshal = marshal(qry_cart, Cart.response_field)

        qry_item = Item.query.get(cart_marshal['item_id'])
        item_marshal = marshal(qry_item, Item.response_field)

        qry_user = User.query.get(cart_marshal['user_id'])
        user_marshal = marshal(qry_user, User.response_field)

        qry_owner = User.query.get(item_marshal['post_by'])
        owner_marshal = marshal(qry_owner, User.response_field)

        transaction = Transaction(item_marshal['id'],item_marshal['name'],item_marshal['urlimages'],item_marshal['harga'],user_marshal['id'],user_marshal['name'],user_marshal['alamat'],user_marshal['urlimage'],item_marshal['post_by'],owner_marshal['name'],owner_marshal['alamat'],owner_marshal['urlimage'],cart_marshal['qty'],"success",str(currentDT),"undeliver")
        db.session.add(transaction)

        
        if (cart_marshal['qty'] > item_marshal['stok']):
            return {'status': 'Failed', 'Pesan': "STOK TIDAK CUKUP" }, 200, {'Content_type': 'application/json'}


        qry_item.stok = item_marshal['stok'] - cart_marshal['qty']
        qry_item.terjual = item_marshal['terjual'] + cart_marshal['qty']
        qry_cart.status = 'PAID'
        qry_owner.transaction = owner_marshal['transaction'] +1
        db.session.commit()
        
        return {'status': 'Success', 'Your Item': item_marshal, "owner":owner_marshal}, 200, {'Content_type': 'application/json'}


api.add_resource(TransactionResource, '', '/<transaction_id>')
