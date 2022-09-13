import json

from InnovationCourse import InnovationCourse
from Student import Student
from credentials import token
from CanvasAPI import CanvasAPI
import re

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token)

# Ik gebruik op Windows Fiddler als debugger, moet nog even een manier vinden requests beter te debuggen
# api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)


with open('./../inno-ids.json') as f:
    this_year_id = json.load(f)['main']
    this_year_raw = api.get(f'courses/{this_year_id}')
    this_year = InnovationCourse(this_year_raw['id'], this_year_raw['name'])

def get_students_from_course(inno_course, target_section):
    inno_sections_raw = api.get_pages(f'courses/{inno_course.id}/sections')
    sd_sections = [section['id'] for section in inno_sections_raw if re.match(target_section, section['name'])]
    inno_enrolments_raw = api.get_pages(f'courses/{inno_course.id}/enrollments', page_size=100)
    students = []
    for inno_enrolment_raw in inno_enrolments_raw:
        if inno_enrolment_raw['course_section_id'] in sd_sections:
            student = Student(inno_enrolment_raw['user']['id'], inno_enrolment_raw['user']['name'])
            student.sections.append(target_section)
            students.append(student)
    return students

sd_students = get_students_from_course(this_year, 'SD')
print(*sd_students)
