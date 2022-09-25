class Assignment:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_json(self):
        return {
            'name': self.name,
            'id': self.id
        }

    @staticmethod
    def from_dict(data_dict):
        return Assignment(data_dict['id'], data_dict['name'])
