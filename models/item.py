import sys, os
sys.path.insert(0, os.path.abspath(__file__+'/../../'))
""" 
sys.path.insert(0, os.path.abspath(__file__+'/../'))
print('')
print(' ... path = ' + os.path.abspath(__file__+'/../../')) 
"""
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))    # la clave es una clave externa; la principal es del store
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name=name).first()     #query = "SELECT * FROM items WHERE name=name LIMIT 1"
        """ 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))   # el segundo parámetro debe ser una tupla, por tanto debemos poner una coma al final
        row = result.fetchone()                   # como no se puede repetir el nombre, como mucho habrá un resultado (no tengo que preocuparme por múltiples resultados)
        connection.close()

        if row:
            return cls(*row)                      #return cls(row[0], row[1])       #return {'item': {'name': row[0], 'price': row[1]}} 
        """
        

    """ 
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
                
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
                
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()
    """

    def save_to_db(self):       # este método sirve tanto para insert como para update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()