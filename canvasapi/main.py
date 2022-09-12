import json

from credentials import token
from CanvasAPI import CanvasAPI
import re

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)
#
# with open('./../inno-data.json') as f:
#     print(list(map(lambda p: p['id'], json.load(f)['projects'])))

#
# inno_sections_raw = api.get_pages('courses/32665/sections')
#
# sd_sections = [section for section in inno_sections_raw if re.match("SD", section['name'])]
# print(sd_sections)
#
# inno_enrolments_raw = api.get_pages('courses/32665/enrollments', page_size=50)
#
# for inno_enrolment_raw in inno_enrolments_raw:
#     if "Daan" in inno_enrolment_raw['user']['name']:
#         print(inno_enrolment_raw)
