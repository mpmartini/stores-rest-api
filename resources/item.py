from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

import sys, os
sys.path.insert(0, os.path.abspath(__file__+'/../../'))     #sys.path.insert(0, "C:\Pi-Fiware\ADEJE_Maqueta\section_6\code")
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id', 
        type=int,
        required = True,
        help = "Every item needs a store id!"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)   #item = next(filter(lambda x: x['name'] == name, items), None)     # next me da el primer elemento de la lista del filtro y 'None' es el valor por defecto
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):                                                         #if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400  # 400 is 'BAD REQUEST' (porque el cliente debería haber comprobado antes que no existía)

        data = Item.parser.parse_args()
        #item = ItemModel(name, data['price'], data['store_id'])            #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, **data) 

        try:
            item.save_to_db()
        except:
            return  {'message': 'An error ocurred inserting the item.'}, 500                # Internal Sever Error
        return item.json(), 201                    # 201 is for 'CREATED'      # 202 is for creation takes too time, so the client don't need to wait 


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()                                       
        item = ItemModel.find_by_name(name)      #item = next(filter(lambda x: x['name'] == name, items), None)  
        if item is None:
            #item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data) 
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()
        """ 
        updated_item = ItemModel(name, data['price'])            #updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                updated_item.insert()           #ItemModel.insert(updated_item)                
            except:
                return  {'message': 'An error ocurred inserting the item.'}, 500
        else:
            try:
                updated_item.update()           #ItemModel.update(updated_item)          
            except:
                return  {'message': 'An error ocurred updating the item.'}, 500        
        return updated_item.json()                    # 201 is for 'CREATED'      # 202 is for creation takes too time, so the client don't need to wait 
        """


    @jwt_required()
    def delete(self, name):        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "Item deleted."}    
        """
        connection = sqlite3.connect('data.db')     
        cursor = connection.cursor()
                
        query = "DELETE FROM items WHERE name=?"        #items = list(filter(lambda x: x['name'] != name, items))
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': "Item deleted."}
        """


class ItemList(Resource):
    def get(self):  
        return  {'items': [x.json() for x in ItemModel.query.all()]}  # o también {'items': ItemModel.list(map(lambda x: x.json(), ItemModel.query.all()))}             
        """ connection = sqlite3.connect('data.db')     
        cursor = connection.cursor()
                
        query = "SELECT * FROM items"    
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        # connection.commit()  # No hay que hacer commit porque no hay que salvar nada
        connection.close()
        return {'items': items} """