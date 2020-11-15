users = []

class user():
    user_id = None
    name = ""
    group = None

    def __init__(self, _id, _name):
        self.user_id = _id
        self.name = _name

def recognize_user(id_):
    for user in users:
        return user
    return False

def is_msg_answer(message):
    for user in (user for user in users if user.user_id == message.from_user.id):
        if (user.group == None) or (user.group == "-"):
            return True
    return False
