# types for mptParser

class Lesson():
    __slots__ = "num", "name", "teacher", "is_dynamic"

    def __init__(self, num: int, name: list,
                 teacher: list, is_dynamic: bool):
        self.num = num
        self.name = name
        self.teacher = teacher
        self.is_dynamic = is_dynamic


class Change():
    __slots__ = "num", "replace_from", "replace_to", "time"

    def __init__(self, num: int, _from: str, to: str, time: str):
        self.num = num
        self.replace_from = _from
        self.replace_to = to
        self.time = time


class Day(list):
    def __add__(self, instance: Lesson):
        return Day(list.__add__(self, instance))


class ChangesList(list):
    def __add__(self, instance: Change):
        return ChangesList(list.__add__(self, instance))
