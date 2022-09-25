from .Project import Project


class HolistiqProject(Project):
    def __init__(self, pid, name):
        super(HolistiqProject, self).__init__(pid, name)
        self.outcomes = []

