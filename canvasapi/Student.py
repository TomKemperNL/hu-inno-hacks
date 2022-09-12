class Student:
    def __init__(self, sid, name):
        self.id = sid
        self.name = name
        self.section = None

    def to_json(self):
        return self.__dict__
