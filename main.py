import json

from canvasapi import *
from credentials import token

import re

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token)

# Ik gebruik op Windows Fiddler als debugger, moet nog even een manier vinden requests beter te debuggen
# api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)


with open('inno-ids.json') as f:
    raw = json.load(f)
    this_year_id = raw['main']
    project_ids = raw['projects']
    this_year_raw = api.get(f'courses/{this_year_id}')
    this_year = InnovationCourse(this_year_raw['id'], this_year_raw['name'])

holistiq = HolisticAPI(api, this_year, "SD")
holistiq.init()  # TODO: uitzoeken hoe dit netter kan, zo'n magische method call is niks natuurlijk


def get_assignment_id_by_name(project, name):
    assignments_response = api.get_pages(f'courses/{project.id}/assignments')
    for assignment_response in assignments_response:
        if assignment_response['name'] == name:
            return assignment_response['id']
    return None


def get_grade_student(project, student, aid):
    submissions_response = api.get_pages(f'courses/{project.id}/assignments/{aid}/submissions')
    matching_submission = list(filter(lambda s: s['user_id'] == student.id, submissions_response))
    if len(matching_submission) > 0:
        if matching_submission[0]['submitted_at'] is not None:
            grade = matching_submission[0]['grade']
            if grade == None:
                return '!'
            else:
                return grade
        else:
            return 'X'
    else:
        return '?'


for project in holistiq.projects:
    print(project.name)

    for student in project.students:
        grades = []
        for nr in [1, 2]:
            aid = get_assignment_id_by_name(project, f'Kennis toepassen op HBO-i niveau 2 | Oplevering {nr} — Docent')
            grade = get_grade_student(project, student, aid)
            grades.append(grade)

        print(f'{student.name:30} - {grades[0]:15} - {grades[1]:15}')
