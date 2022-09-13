from .context import *
from canvasapi import parse_links


def test_parse_links():
    header = '<https://canvas.hu.nl/api/v1/courses?page=1&per_page=10>; rel="current",<https://canvas.hu.nl/api/v1/courses?page=2&per_page=10>; rel="next",<https://canvas.hu.nl/api/v1/courses?page=1&per_page=10>; rel="first",<https://canvas.hu.nl/api/v1/courses?page=5&per_page=10>; rel="last"'
    result = parse_links(header)
    assert 'next' in result.keys()
    assert result['next'] == 'https://canvas.hu.nl/api/v1/courses?page=2&per_page=10'
