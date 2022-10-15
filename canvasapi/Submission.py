from .Student import *


class Submission:
    def __init__(self, assignment_id, attempt, submitted_at, grade=None, rubric=None):
        if rubric is None:
            rubric = {}

        self.assignment_id = assignment_id
        self.attempt = attempt
        self.submitted_at = submitted_at
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
            #todo, dicts naar json? zou makkelijk moeten zijn...
        }

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
