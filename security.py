
# Este fichero pretende llevar una BD de usuarios
#from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate (username, password):
    user = UserModel.find_by_username(username)    
    if user and (user.password==password):   # safe_str_cmp(user.password,password):  para comparar cadenas de texto con la versión werzeug==2.0.0 (hacer "pip install Werkzeug==2.0.0")
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)