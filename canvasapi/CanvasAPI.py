import re

import requests


def parse_links(links_header):
    result = {}
    parts = [p.strip() for p in links_header.split(',')]
    for p in parts:
        split = p.split(';')
        key = re.match('rel="(\\w+)"', split[1].strip())[1]
        value = split[0].removeprefix('<').removesuffix('>')
        result[key] = value
    return result


def bearer_auth(token):
    def with_header(req):
        req.headers["Authorization"] = "Bearer " + token
        return req

    return with_header


class CanvasAPI:
    def _get_basic_args(self):
        args = {'auth': bearer_auth(self.token)}
        if self.proxy is not None:
            args['proxies'] = {'http': self.proxy, 'https': self.proxy}
            args['verify'] = False

        return args

    def __init__(self, base_url, token, proxy=None):
        self.base_url = base_url + 'api/v1/'
        self.bare_url = base_url
        self.proxy = proxy
        self.token = token

    def _get_raw(self, full_url, query_args={}):
        response = requests.get(full_url, params=query_args, **self._get_basic_args())
        return response

    def get(self, url):
        full_url = self.base_url + url
        return self._get_raw(full_url).json()

    def create_api_url(self, relative_url):
        return self.base_url + relative_url

    def create_client_url(self, relative_url):
        return self.bare_url + relative_url

    def get_pages(self, url, *, page_size=10):
        extra_args = {}
        if page_size:
            extra_args['per_page'] = page_size

        full_url = self.base_url + url
        response = self._get_raw(full_url, query_args=extra_args)
        result = response.json()

        def has_next_page(response):
            if 'Link' in response.headers.keys():
                return 'next' in parse_links(response.headers['Link'])
            else:
                return False

        while has_next_page(response):
            links = parse_links(response.headers['Link'])
            response = self._get_raw(links['next'])
            result = result + response.json()
        return result
