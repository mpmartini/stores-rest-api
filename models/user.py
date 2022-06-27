import sys, os
sys.path.insert(0, os.path.abspath(__file__+'/../../'))
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)        # id es primary_key, así que es incremental, así que la BD asignará un id automáticamente.
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):             # no es necesario dar un id aquí porque es autogenerado
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):                    # antes de declararlo como método de clase esto sería "def find_by_username(self, username):"
        return cls.query.filter_by(username=username).first()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            #user = cls(row[0], row[1], row[2])              # antes de declararlo como método de clase esto sería "user = User(row[0], row[1], row[2])"
            user = cls(*row)                                 # como los parámetros (row[0], row[1], row[2]) están en orden (_id, username, password) se puede poner "*row"
        else:
            user = None
        connection.close()
        return user
        """

    @classmethod
    def find_by_id(cls, _id):  
        return cls.query.filter_by(id=_id).first()                  
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)                                   
        else:
            user = None
        connection.close()
        return user
        """