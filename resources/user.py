import sqlite3
from flask_restful import Resource, reqparse

import sys, os
#sys.path.insert(0, "C:\Pi-Fiware\ADEJE_Maqueta\section_6\code")
sys.path.insert(0, os.path.abspath(__file__+'/../../'))  #para ir del directorio "C:\Pi-Fiware\ADEJE_Maqueta\section_6\code\resources" al "C:\Pi-Fiware\ADEJE_Maqueta\section_6\code"
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
        )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that surname already exists"}, 400

        user = UserModel(**data)    #user = UserModel(data['username'], data['password'])  como usamos un parser, ya sabemos que en dat viene un username y un password, así que podemos poner **data
        user.save_to_db()

        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        """

        return {"message": "user created successfully."}, 201

