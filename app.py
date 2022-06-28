from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'         # cambiando sqlite por MySQL, Oracle, etc. funcionaría igual con otro tipo de bases de datos.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # para que no consuma recursos al hacer el tracking de todas las modificaciones que se hacen sin salvar
app.secret_key = 'qqwwee'   
api = Api(app)

jwt = JWT(app, authenticate, identity)      # /auth

api.add_resource(Item, '/item/<string:name>')  #http://127.0.0.1:5000/item/piano
api.add_resource(ItemList, '/items') 
api.add_resource(Store, '/store/<string:name>')  #http://127.0.0.1:5000/store/instruments
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":                  #este if hace que si hacemos un import de este fichero, no arranque la aplicación. Solo la arrancaría si se ejecuta el fichero.py
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)