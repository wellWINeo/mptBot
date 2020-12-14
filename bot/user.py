from enum import IntEnum, auto
from tinydb import Query, TinyDB

class status(IntEnum):
    UNKNOWN = auto()    # new user, just created
    NO_GROUP = auto()   # user w/o group
    ANON = auto()       # no logged in user, request shedule for group
    ANOTHER = auto()    # logged in user requested shedule for another gorup
    COMPLETE = auto()   # all user's filed filled


class user:
    user_id: int
    name: str
    group = ""
    last_chat_id: str
    comm = str()

    def __init__(self, _id, _name, _chat, _group=None, _status=status.UNKNOWN):
        self.user_id = _id
        self.name = _name
        self.last_chat_id = _chat
        self.group = _group
        self.status = _status


class users_db():
    db = None
    query = Query()

    def __init__(self, path):
        self.db = TinyDB(path)

    def get_user(self, _id):
        json_data = self.db.get(self.query.user_id == _id)
        if json_data != None:
            response = user(json_data["user_id"], json_data["name"], 
                            json_data["last_chat_id"])
            response.group = json_data["group"]
            response.status = status(json_data["status"])
            return response
        return None
        
    def add_user(self, instance):
        self.db.insert({
            "user_id": instance.user_id,
            "name" : instance.name,
            "group": instance.group,
            "last_chat_id": instance.last_chat_id,
            "status": instance.status.value})

    def del_user(self, _id):
        self.db.remove(self.query.user_id == _id)

    def update(self, instance):
        self.db.update({"user_id": instance.user_id,
                        "name": instance.name,
                        "group": instance.group,
                        "last_chat_id": instance.last_chat_id,
                        "status": instance.status},
                        self.query.user_id == instance.user_id)

