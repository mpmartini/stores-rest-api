import sys, os
sys.path.insert(0, os.path.abspath(__file__+'/../../'))
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #items = db.relationship('ItemModel')                   # relación con la tabla ItemModel (un item tiene un store, pero un store puede tener muchos items) => items es una lista
    items = db.relationship('ItemModel', lazy='dynamic')    #ahora items ya no es una lista, sino una query inside ItemModel       # con lazy='dynamic, le decimos que no cree un objeto para cada elemento de la tabla hasta que no sea necesario (hasta que no se llame al método json)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items':[item.json() for item in self.items.all()]}  # se crea lazy='dynamic' y mira en la tabla cuando lo necesita

    @classmethod
    def find_by_name(cls, name):        
        print(' ... modeles/StoreModel.find_by_name('+ name +')')
        return cls.query.filter_by(name=name).first()     #query = "SELECT * FROM items WHERE name=name LIMIT 1"

    def save_to_db(self):       # este método sirve tanto para insert como para update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()