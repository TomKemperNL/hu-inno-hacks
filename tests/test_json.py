from InnovationCourse import *
from Project import *
from Student import *


def test_serialize_json():
    course = InnovationCourse(123, 'Innovation Test')
    student = Student(456, 'Tom Test')
    project = Project(789, 'Pielen in Python')
    project.students.append(student)
    course.projects.append(project)

    generated_dict = course.to_json()
    reassembled = InnovationCourse.from_dict(generated_dict)

    # TODO: uitzoeken hoe je equals netjes fixt in Python... want dit is terror
    assert reassembled.id == course.id
    assert reassembled.projects[0].id == course.projects[0].id
    assert reassembled.projects[0].students[0].id == course.projects[0].students[0].id
