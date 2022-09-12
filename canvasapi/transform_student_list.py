import json

students = []

with open('../students_per_project.json', 'r') as f:
    raw_data = json.load(f)
    for p in raw_data:
        for s in p['students']:
            students.append((p['name'], s['name']))

sorted_students = list(sorted(students, key=lambda s: s[1]))

with open('./../students-project.json', 'w') as f:
    json.dump(sorted_students, f)