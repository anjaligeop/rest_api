from models.user import UserModel
from werkzeug.security import safe_str_cmp
'''
users = [
   User(1,'bob','asdf')
]

username_mapping = {u.username : u for u in users}# key = username, value = user object

userid_mapping = {u.id : u for u in users}
'''
def authenticate(username,password):
    #user = username_mapping.get(username,None) #get is a method of retreiving elements in dict, None if not present
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password , password):
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_mapping.get(user_id,None)
    return UserModel.find_by_id(user_id)