import json

from canvasapi import *
from credentials import token
import datetime

import re

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/', token)

# Ik gebruik op Windows Fiddler als debugger, moet nog even een manier vinden requests beter te debuggen
# api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)


with open('inno-ids.json') as f:
    raw = json.load(f)
    this_year_id = raw['main']
    project_ids = raw['projects']
    this_year_raw = api.get(f'courses/{this_year_id}')
    this_year = InnovationCourse(this_year_raw['id'], this_year_raw['name'])

holistiq = HolisticAPI(api, this_year, "SD")
holistiq.init(project_ids)  # TODO: uitzoeken hoe dit netter kan, zo'n magische method call is niks natuurlijk

all_todos = []
for project in holistiq.projects:
    (grades_per_student, todos) = holistiq.get_grades_in_project(project, [
        'Kennis toepassen op HBO-i niveau 2',
        'Nieuwe competenties op HBO-i niveau 3',
        'Gedreven ontwerpen',
        'Gedistribueerde systemen'
    ])
    all_todos = all_todos + todos

    print(project.name)
    for student in grades_per_student.keys():
        print('\t' + student)
        total_submissions = 0
        last_submission = None
        for assignment in grades_per_student[student].keys():
            submissions = grades_per_student[student][assignment]
            total_submissions += len(submissions.values())

            grades_per_criteria = {}
            if submissions is not None and len(submissions) > 0:
                for submission in submissions.values():
                    for (key, graded_criterion) in submission.rubric.items():
                        if key not in grades_per_criteria.keys():
                            grades_per_criteria[key] = []

                        if 'points' in graded_criterion.keys():
                            grades_per_criteria[key].append(graded_criterion['points'])
                    last = max(map(lambda s: s.submitted_at, submissions.values()))
                    last_submission = last if last_submission is None else max([last_submission, last])

            print(f'\t\t{assignment}: ')
            for (criterion, grades) in grades_per_criteria.items():
                print(f'\t\t\t{criterion:135}: {", ".join(list(map(str, grades)))}')
        print('')
        print(f'\t\tAantal opleveringen: {total_submissions}')
        last_formatted = "-" if last_submission is None else last_submission.strftime("%d %b")
        print(f'\t\tLaatste opleveringen: {last_formatted}')

for todo in all_todos:
    print(todo)
