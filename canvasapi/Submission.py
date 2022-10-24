from .Student import *
import datetime
from .Criterion import Criterion


class Submission:
    def __init__(self, assignment_id, attempt, submitted_at, grade=None, rubric=None):
        if rubric is None:
            rubric = {}

        self.assignment_id = assignment_id
        self.attempt = attempt
        self.submitted_at = datetime.datetime.strptime(submitted_at, '%Y-%m-%dT%H:%M:%SZ')
        self.grade = grade
        if self.grade is None:
            self.grade = '!'
        self.rubric = rubric

    def to_json(self):
        return {
            'assignment_id': self.name,
            'attempt': self.id,
            'submitted_at': self.submitted_at,
            'grade': self.grade
            # todo, dicts naar json? zou makkelijk moeten zijn...
        }

    def fix_rubrics(self, rubric_list):
        old_rubric = self.rubric
        self.rubric = {}
        for k in old_rubric.keys():
            key = Criterion.fix_id(k)
            for rubric in rubric_list:
                matching_criteria = list(filter(lambda r: r.id == key, rubric.criteria))
                if len(matching_criteria) > 0:
                    self.rubric[matching_criteria[0].name] = old_rubric[k]

    @staticmethod
    def from_dict(data_dict):
        rubric = {}
        if 'rubric_assessment' in data_dict.keys():
            rubric = data_dict['rubric_assessment']

        return Submission(
            data_dict['assignment_id'],
            data_dict['attempt'],
            data_dict['submitted_at'],
            data_dict['grade'],
            rubric
        )
