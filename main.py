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


get_students_cached = cache_list("sd_students.json", Student, get_students_from_course)


def get_inno_projects(ids, all_students):
    courses = []
    for course_id in ids:
        course_response = api.get_pages(f'courses/{course_id}')
        course = Project(course_response['id'], course_response['name'])
        print(course.name)
        enrollments = api.get_pages(f'courses/{course_id}/enrollments')
        for enrollment_resp in enrollments:
            if enrollment_resp['type'] == "StudentEnrollment":
                matching_students = list(filter(lambda s: s.id == enrollment_resp['user']['id'], all_students))
                if len(matching_students) == 1:
                    course.students.append(matching_students[0])

        courses.append(course)
    return courses


get_inno_projects_cached = cache_list("all_projects.json", Project, get_inno_projects)

sd_students = get_students_cached(this_year, 'SD')
projects = get_inno_projects_cached(project_ids, sd_students)



print(projects[0].students[1])

