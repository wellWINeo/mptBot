import config
import bot.handlers as handlers 
from tinydb import TinyDB, Query

users_db = TinyDB(config.db_path)

User = Query()

def add_user(instance):
    users_db.insert({
                     "user_id" : instance.user_id,
                     "name" : instance.name,
                     "group" : instance.group
                     })

def remove_user(_id):
    users_db.remove(User.id == _id)

def load():
    response = []
    if len(users_db.all()) != 0:
        for user in users_db:
            response.append(handlers.user(user["user_id"], user["name"],
                                          user["group"]))
    return response
