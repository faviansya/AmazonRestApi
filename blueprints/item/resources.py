import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from . import *
from ..user import *
from ..cart import *
from  sqlalchemy.sql.expression import func, select
import datetime

from sqlalchemy import desc

bp_item = Blueprint('item', __name__)
api = Api(bp_item)

class ItemResource(Resource):

    def __init__(self):
        pass
        
    @jwt_required
    def get(self, item_id = None):
        jwtclaim = get_jwt_claims()
        if item_id == None or item_id == 'all':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('item_id', type = int, location = 'args')
            parser.add_argument('user_id',type =int, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Item.query

            if args['user_id'] is not None:
                qry = qry.filter(Item.post_by.like(args['user_id'])).all()
                qryUser = User.query.get(args['user_id'])
                if qry == None:
                    return {"Status":"Success","DataUser":marshal(qryUser, User.response_field), "DataItem":[]}, 200, {'Content_type' : 'application/json'} 
                qryUser = User.query.get(args['user_id'])
                return {"Status":"Success","DataUser":marshal(qryUser, User.response_field), "DataItem":marshal(qry, Item.response_field)}, 200, {'Content_type' : 'application/json'} 

            if args['item_id'] is not None:
                qry = qry.get(args['item_id'])
                qryUser = User.query.get(marshal(qry, Item.response_field)['post_by'])
                return {"Status":"Success","Item": marshal(qry, Item.response_field),"user":marshal(qryUser, User.response_field)}, 200, {'Content_type' : 'application/json'} 

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Item.response_field))

            return {"data":rows}, 200, {'Content_type' : 'application/json'}

        elif (item_id == 'myitems'):
            if(jwtclaim['level'] is not 'admin'):
                qry = Item.query.filter(Item.post_by.like(jwtclaim['id'])).all()
                return marshal(qry, Item.response_field), 200, {'Content_type' : 'application/json'}
            return {'status' :"you Are Admin, You Dont Have Privileage to SELL something"}, 402, {'Content_type' : 'application/json'}
        
        elif (item_id == 'bestitem'):
            if(jwtclaim['level'] is not 'admin'):
                qry = Item.query.order_by(desc(Item.terjual)).limit(3).all()

                rows = []
                # for row in qry:
                #     rows.append(marshal(row, Item.response_field))

                return marshal(qry, Item.response_field), 200, {'Content_type' : 'application/json'}
            return {'status' :"you Are Admin, You Dont Have Privileage to SELL something"}, 402, {'Content_type' : 'application/json'}
        
        elif (item_id == 'home'):
            qry = Item.query.order_by(func.random()).limit(6).all()
            rows = []
            for row in qry:
                rows.append(marshal(row, Item.response_field))

            return {"data":rows}, 200, {'Content_type' : 'application/json'}

        elif (item_id == 'kategori'):
            parser = reqparse.RequestParser()
            parser.add_argument('kategori', location = 'args')
            args = parser.parse_args()

            qry = Item.query.filter(Item.kategori.like(args['kategori'])).all()
            # rows = []
            # for row in qry:
            #     rows.append(marshal(row, Item.response_field))
            return {"data":marshal(qry, Item.response_field)}, 200, {'Content_type' : 'application/json'}
        
        elif (item_id == 'search'):
            parser = reqparse.RequestParser()
            parser.add_argument('nama', location = 'args')
            args = parser.parse_args()

            qry = Item.query.filter(Item.name.like("%"+args['nama']+"%")).all()
            # rows = []
            # for row in qry:
            #     rows.append(marshal(row, Item.response_field))

            return {"data":marshal(qry, Item.response_field)}, 200, {'Content_type' : 'application/json'}

        else:
            qry = Item.query.get(item_id)
            qryUser = User.query.get(marshal(qry, Item.response_field)['post_by'])
            if qry is not None:
                return {"Status":"Success","Item": marshal(qry, Item.response_field),"user":marshal(qryUser, User.response_field)}, 200, {'Content_type' : 'application/json'} 
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'Incorrect ID'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args',required = True)
        args = parser.parse_args()

        qry = Item.query.get(args['id'])
        qryCart = Cart.query.filter(Cart.item_id.like(marshal(qry, Item.response_field)["id"])).all()

        if(jwtclaim['level'] == 'user'):
            if jwtclaim['id'] == marshal(qry, Item.response_field)['post_by']:
                db.session.delete(qry)
                db.session.commit()
                for row in qryCart:
                    db.session.delete(row)
                    db.session.commit()
                return {'status' : 'Success', 'message' : 'Your Own Data has Been Deleted'}, 200, {'Content_type' : 'application/json'}
        
        elif(jwtclaim['level'] == 'admin'):
            db.session.delete(qry)
            db.session.commit()
            for row in qryCart:
                db.session.delete(row)
                db.session.commit()
            return {'status' : 'Success', 'message' : 'Admin Delete Choosen Data'}, 200, {'Content_type' : 'application/json'}
        # return {'status' : rows, 'message' : 'Not Your Items, You Only Can Choose Your Item'}, 404, {'Content_type' : 'application/json'}

        return {'status' : 'Failed', 'message' : 'Not Your Items, You Only Can Choose Your Item'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int, location = 'args', required = True)
        args = parser.parse_args()
        qry_item = Item.query.get(args['id'])

        if jwtclaim['level'] == 'user':
            if jwtclaim['id'] != marshal(qry_item, Item.response_field)['post_by']:
                return {'status' : 'Failed', 'Your ID' : 'Not Your Item'}, 200, {'Content_type' : 'application/json'}

        item_marshal = marshal(qry_item, Item.response_field)
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int, location = 'args', required = True)
        parser.add_argument('nama', location = 'json', default = item_marshal['name'])
        parser.add_argument('urlimage', location = 'json', default = item_marshal['urlimages'])
        parser.add_argument('harga', location = 'json', default = item_marshal['harga'])
        parser.add_argument('kategori', location = 'json',default = item_marshal['kategori'])
        parser.add_argument('kondisi', location = 'json',default = item_marshal['kondisi'])
        parser.add_argument('deskripsi', location = 'json',default = item_marshal['deskripsi'])
        parser.add_argument('berat', location = 'json',default = item_marshal['berat'])
        parser.add_argument('stok', location = 'json',default = item_marshal['stok'])
        parser.add_argument('kadaluwarsa', location = 'json',default = item_marshal['kadaluwarsa'])
        args = parser.parse_args()
        
        qry_item.name = args['nama']
        qry_item.urlimages = args['urlimage']
        qry_item.harga = args['harga']
        qry_item.kategori = args['kategori']
        qry_item.kondisi = args['kondisi']
        qry_item.deskripsi = args['deskripsi']
        qry_item.berat = args['berat']
        qry_item.stok = args['stok']
        qry_item.kadaluwarsa = args['kadaluwarsa']
        db.session.commit()

        qry_item = Item.query.get(args['id'])
        item_marshal = marshal(qry_item, Item.response_field)
        qryCart = Cart.query.filter(Cart.item_id.like(item_marshal["id"])).all()

        rows = []
        for row in qryCart:
            rows.append(marshal(row, Cart.response_field))
            row.itemname = item_marshal['name']
            row.harga = item_marshal['harga']
            row.berat = item_marshal['berat']
            row.urlimage = item_marshal['urlimages']
            db.session.commit()
            
        return {'status' : rows, 'Your Item' : marshal(qry_item, Item.response_field)}, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        currentDT = datetime.datetime.now()
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            parser = reqparse.RequestParser()
            parser.add_argument('nama', location = 'json', required = True)
            parser.add_argument('urlimage', location = 'json',required = True)
            parser.add_argument('harga', location = 'json', required = True)
            parser.add_argument('kategori', location = 'json', required = True)
            parser.add_argument('kondisi', location = 'json', default = 'baru',required = True)
            parser.add_argument('deskripsi', location = 'json', required = True )            
            parser.add_argument('berat', location = 'json', default = 100)
            parser.add_argument('stok', default = 1)
            parser.add_argument('kadaluwarsa', default = "None")
            args = parser.parse_args()

            item = Item(args['nama'],args['urlimage'], args['harga'],args['kategori'],args['kondisi'],
                        args['deskripsi'],'published',args['berat'],args['stok'],args['kadaluwarsa'],0, jwtclaim['id'], str(currentDT))
            db.session.add(item)
            db.session.commit()

            return {'status' : 'Success', 'Your Account' : marshal(item, Item.response_field)}, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'Failed', 'message' : 'You Are Admin Not Allowed To Sell'}, 401, {'Content_type' : 'application/json'}


api.add_resource(ItemResource, '', '/<item_id>')