# types for mptParser
# from marshmallow_dataclasss import dataclass
from enum import Enum
import json

class LessonEncoder:
    def __init__ (self, data):
        vars(self).update(data)

# @dataclass
class Lesson():
    __slots__ = "num", "name", "teacher", "is_dynamic"

    def __init__(self, num: int, name: list,
                 teacher: list, is_dynamic: bool):
        self.num = num
        self.name = name
        self.teacher = teacher
        self.is_dynamic = is_dynamic

    @classmethod
    def from_json(cls, json_data):
        return json.loads(json_data, object_hook=cls.as_json)   

    @classmethod
    def as_json(cls, dct):
        return cls(dct['num'], dct['name'],
                   dct['teacher'], dct['is_dynamic'])

    def to_json(self):
        return json.dumps({
            'num': self.num,
            'name': self.name,
            'teacher': self.teacher,
            'is_dynamic': self.is_dynamic
            })

    def show(self):
        print(f"num: {self.num}")
        if self.is_dynamic:
            print(f"teacher #1: {self.teacher[0]}")
            print(f"name #1: {self.name[0]}")
            print("----")
            print(f"teacher #2: {self.teacher[1]}")
            print(f"name #2: {self.name[1]}")
        else:
            print(f"teacher: {self.teacher}")
            print(f"name: {self.name}")

        print(f"Dynamic: {self.is_dynamic}")


class Change():
    __slots__ = "num", "replace_from", "replace_to", "time"

    def __init__(self, num: int, _from: str, to: str, time: str):
        self.num = num
        self.replace_from = _from
        self.replace_to = to
        self.time = time

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data)

    def to_json(self):
        return json.dumps({
            'num': self.num,
            'replace_from': self.replace_from,
            'replace_to': self.replace_to,
            'time': self.time
            })


class Day(list):
    def __add__(self, instance: Lesson):
        return Day(list.__add__(self, instance))


class ChangesList(list):
    def __add__(self, instance: Change):
        return ChangesList(list.__add__(self, instance))


class WeekNum(Enum):
    NotFound = 0,
    Chisl = 1,
    Znam = 2,


Directions = (
        "09.02.01", "09.02.02", "09.02.03", "09.02.04",
        "09.02.05", "09.02.06", "09.02.07", "10.02.03",
        "10.02.05", "40.02.01", "Отделение первого курса"
        ) 
