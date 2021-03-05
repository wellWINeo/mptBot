from enum import Enum, auto
from tinydb import Query, TinyDB


class status(Enum):
    UNKNOWN = auto()
    NO_GROUP = auto()
    COMPLETE = auto()


class user:
    user_id: int
    name: str
    group: str
    last_chat_id: str
    status = status.UNKNOWN
    
    def __init__(self, _id, _name):
        self.user_id = _id
        self.name = _name


class users_db:
    db: TinyDB()
    query = Query()

    def __init__(self, path):
        self.db = TinyDB(path)

    def get_user(self, _id):
        return self.db.get(self.query.user_id == _id)

    def add_user(self, instance):
        self.db.insert({
            "user_id": instance.user_id,
            "name": instance.name,
            "group": instance.group,
            "last_chat_id": instance.last_chat_id,
            "status": instance.status})

    def del_user(self, _id):
        self.db.remove(self.query.user_id == _id)

    def update(self, instance):
        self.db.update({"user_id": instance.user_id,
                        "name": instance.name,
                        "group": instance.group,
                        "last_chat_id": instance.last_chat_id,
                        "status": instance.status},
                        self.query.user_id == instance.user_id)
