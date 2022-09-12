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
