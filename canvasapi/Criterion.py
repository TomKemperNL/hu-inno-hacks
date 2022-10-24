class Criterion:
    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.points = points

    def to_json(self):
        return {
            'description': self.name,
            'id': f'_{self.id}',
            'points': self.points
        }

    @staticmethod
    def from_dict(data_dict):
        return Criterion(Criterion.fix_id(data_dict['id']), data_dict['description'], int(data_dict['points']))

    @staticmethod
    def fix_id(raw_id):
        return int(raw_id.replace('_', ''))
