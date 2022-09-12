class Student:
    def __init__(self, sid, name):
        self.id = sid
        self.name = name
        self.sections = []

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_dict(data_dict):
        new_student = Student(data_dict['id'], data_dict['name'])
        new_student.sections = new_student.sections + data_dict['sections']
        return new_student
