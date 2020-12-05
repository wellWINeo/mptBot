class user():
    user_id: int
    name: str
    group: str

    def __init__(self, _id, _name, _group=None):
        self.user_id = _id
        self.name = _name
        self.group = _group
