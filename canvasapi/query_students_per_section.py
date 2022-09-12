from credentials import token
from CanvasAPI import CanvasAPI
from pathlib import Path
from Project import *
from Student import *
import json

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token)

main_course_id = None
with open('./../inno-data.json') as f:
    inno_data = json.load(f)
    main_course_id = inno_data['main']['id']


with open('../students_per_section.json', 'w') as f:
    json.dump(list(map(lambda c: c.to_json(), courses)), f)
