import re

from .Student import Student
from .Project import Project
from .Caching import cache_list
from .Assignment import Assignment


class HolisticAPI:
    def __init__(self, canvas_api, inno_course, programme):
        self.canvas_api = canvas_api
        self.innovation_course = inno_course
        self.programme = programme
        self.projects = []
        self.students = []

    def init(self, project_ids):
        def get_students_from_course(inno_course, target_section):
            inno_sections_raw = self.canvas_api.get_pages(f'courses/{inno_course.id}/sections')
            sd_sections = [section['id'] for section in inno_sections_raw if re.match(target_section, section['name'])]
            inno_enrolments_raw = self.canvas_api.get_pages(f'courses/{inno_course.id}/enrollments', page_size=100)
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
                course_response = self.canvas_api.get_pages(f'courses/{course_id}')
                course = Project(course_response['id'], course_response['name'])
                enrollments = self.canvas_api.get_pages(f'courses/{course_id}/enrollments')
                for enrollment_resp in enrollments:
                    if enrollment_resp['type'] == "StudentEnrollment":
                        matching_students = list(filter(lambda s: s.id == enrollment_resp['user']['id'], all_students))
                        if len(matching_students) == 1:
                            course.students.append(matching_students[0])

                courses.append(course)
            return courses

        get_inno_projects_cached = cache_list("all_projects.json", Project, get_inno_projects)

        self.students = get_students_cached(self.innovation_course, 'SD')
        self.projects = get_inno_projects_cached(project_ids, self.students)

    def get_project(self, name):
        for p in self.projects:
            if str(name) in p.name:
                return p
        return None

    def get_grades_in_project(self, project, assignment_names):

        def get_assignments_from_project(pjt):
            assignments_response = self.canvas_api.get_pages(f'courses/{pjt.id}/assignments')
            assignments = list(map(lambda a: Assignment.from_dict(a), assignments_response))
            return assignments

        def cached_get_assignments_from_project(pjt):
            cached_wrapper = cache_list(f'assignments_{pjt.id}.json', Assignment, get_assignments_from_project)
            return cached_wrapper(pjt)

        def get_assignment_ids_by_name(project, name):
            assignments = cached_get_assignments_from_project(project)
            ids = []
            for assignment in assignments:
                if assignment.name == name:
                    ids.append(assignment.id)
            return ids

        in_memory_submissions_cache = {}

        def get_grade_student(project, student, aid):
            key = f'{project.id}-{aid}'
            if key not in in_memory_submissions_cache.keys():
                in_memory_submissions_cache[key] = self.canvas_api.get_pages(
                    f'courses/{project.id}/assignments/{aid}/submissions')

            submissions_response = in_memory_submissions_cache[key]

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

        todos = []
        result = {}
        for student in project.students:
            result[student.name] = {}
            for name in assignment_names:
                grades = {}
                result[student.name][name] = grades
                for nr in range(1, 10):
                    assignment_name = f'{name} | Oplevering {nr} — Docent'
                    assignment_ids = get_assignment_ids_by_name(project,
                                                                assignment_name)
                    for aid in assignment_ids:
                        if aid is not None:
                            grade = get_grade_student(project, student, aid)
                            if grade == '!':
                                todos.append({
                                    'project': project.name,
                                    'student': student.name,
                                    'assignment': assignment_name,
                                    'link': self.canvas_api.create_client_url(
                                        f'/courses/{project.id}/gradebook/speed_grader?assignment_id={aid}&student_id={student.id}')
                                })

                            if nr in grades.keys():
                                if grade not in ['!', 'X', '?']:
                                    grades[nr] = grade
                            else:
                                if grade not in ['X', '?']:
                                    grades[nr] = grade
        return result, todos
