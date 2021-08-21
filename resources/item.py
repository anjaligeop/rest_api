import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel
import json

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store id"
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           return item.json()
        return {"message":"Item not found"},404
   

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':'An item with name {} already exists'.format(name)},400
        
        data = Item.parser.parse_args()
        print(data)
        item = ItemModel(name,**data)#data['price'],data['store_id']
        try:
            #print(item)
            item.save_to_db()
        except Exception as e:
            return {"message":"An error occurred while inserting item"},500 #internal server error
        return item.json(),201
    

    @jwt_required()
    def delete(self, name):        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message":"Item is deleted"}
        else:
            return {"message":"item not found"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()        
        item =ItemModel.find_by_name(name)
        
        if item is None:
           item = ItemModel(name,data['price'],data['store_id'])          
        else:
            item.price = data['price']
        item.save_to_db()
        return {"updated item ":item.json()}

   
class ItemList(Resource):
    def get(self):
        items_obtained = ItemModel.query.all()  
       
        return {'items':[items.json() for items in items_obtained]}