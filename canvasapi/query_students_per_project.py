from credentials import token
from CanvasAPI import CanvasAPI
from pathlib import Path
from Project import *
from Student import *
import json

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token)

ids = []
with open('./../inno-data.json') as f:
    inno_data = json.load(f)
    print(inno_data)
    for p in inno_data['projects']:
        ids.append(p['id'])

courses = []

for course_id in ids:
    course_response = api.get_pages(f'courses/{course_id}')
    course = Project(course_response['id'], course_response['name'])
    print(course.name)
    enrollments = api.get_pages(f'courses/{course_id}/enrollments')
    for enrollment_resp in enrollments:
        if enrollment_resp['type'] == "StudentEnrollment":
            course.students.append(Student(enrollment_resp['user']['id'], enrollment_resp['user']['name']))
    courses.append(course)

with open('../students_per_project.json', 'w') as f:
    json.dump(list(map(lambda c: c.to_json(), courses)), f)
