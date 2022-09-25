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

# for project in holistiq.projects:
#     holistiq.get_grades_in_project(project)
#
# print()
#
#
holistiq.get_grades_in_project(holistiq.get_project(385))