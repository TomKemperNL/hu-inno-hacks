from credentials import token
import requests


def bearer_auth(token):
    def with_header(req):
        print('adding header')
        req.headers["Authorization"] = "Bearer " + token
        return req

    return with_header


courses = requests.get('https://canvas.hu.nl/api/v1/courses', auth=bearer_auth(token),
                       proxies={'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}, verify=False)

for course in courses.json():
    print(course)
    print(type(course))
