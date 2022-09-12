from credentials import token
from CanvasAPI import CanvasAPI

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token)

# for course in api.get_pages('courses'):
#   print(course)


import json

ids = []
with open('./../inno-data.json') as f:
    inno_data = json.load(f)
    print(inno_data)
    for p in inno_data['projects']:
        ids.append(p['id'])

print(ids)