from credentials import token
from CanvasAPI import CanvasAPI

proxy = 'http://localhost:8888'
api = CanvasAPI('https://canvas.hu.nl/api/v1/', token, proxy)

for course in api.get_pages('courses'):
    print(course)