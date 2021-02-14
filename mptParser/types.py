import collections
#

class lesson():
    
    __slots__ = "num", "name", "teacher"

    def __init__(self, num: int, name: str, teacher: str):
        self.num = num
        self.name = name
        self.teacher = teacher


class change():
   
    __slots__ = "num", "replace_from", "replace_to", "time"

    def __init__(self, num: int, _from: str, to: str, time: str):
        self.num = num
        self.replace_from = _from
        self.replace_to = to
        self.time = time


class Day(list):
    def __add__(self, instance: lesson):
        return Day(list.__add__(self, instance))


class Changes(list):
    def __add__(self, instance: change):
        return Changes(list.__add__(self, instance))
