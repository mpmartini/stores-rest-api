from flask_restful import Resource

import sys, os
sys.path.insert(0, os.path.abspath(__file__+'/../../'))     #sys.path.insert(0, "C:\Pi-Fiware\ADEJE_Maqueta\section_6\code")
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        print(' ... resources/Store.get(' + name + ')')
        store = StoreModel.find_by_name(name)
        print(' ... resources/Store.get(' + name + ') ... buscado')
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        print(' ... resources/Store.post(' + name + ')')
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
