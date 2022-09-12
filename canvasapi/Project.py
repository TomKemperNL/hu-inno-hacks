from Student import *


class Project:
    def __init__(self, pid, name):
        self.students = []
        self.name = name
        self.id = pid

    def to_json(self):
        return {
            'name': self.name,
            'id': self.id,
            'students': list(map(lambda s: s.to_json(), self.students))
        }

    @staticmethod
    def from_dict(data_dict):
        new_project = Project(data_dict['id'], data_dict['name'])
        new_project.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        return new_project
