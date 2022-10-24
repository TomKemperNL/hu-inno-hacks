from .Criterion import Criterion


class Rubric:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.criteria = []

    def to_json(self):
        return {
            'title': self.name,
            'id': self.id,
            'data': list(map(lambda c: c.to_json(), self.criteria))
        }

    @staticmethod
    def from_dict(data_dict):
        rubric = Rubric(data_dict['id'], data_dict['title'])
        rubric.criteria = rubric.criteria + list(map(lambda r: Criterion.from_dict(r), data_dict['data']))
        return rubric
