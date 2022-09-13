class Student:
    def __init__(self, sid, name, sections=None):
        self.id = sid
        self.name = name
        self.sections = sections
        if not sections:
            self.sections = []

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return f'Student({self.id}, {self.name}, {self.sections})'

    @staticmethod
    def from_dict(data_dict):
        new_student = Student(data_dict['id'], data_dict['name'])
        new_student.sections = new_student.sections + data_dict['sections']
        return new_student
