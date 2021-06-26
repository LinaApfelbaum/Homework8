"""Utils module."""

import re
from http import HTTPStatus


def parse_method(status_line):
    """
    Parse method from status line
    """
    status_line_parts = status_line.split(' ')
    if len(status_line_parts) > 1:
        return status_line_parts[0]

    return ''


def parse_status_code(status_line):
    """
    Parse status code from status line
    """
    matches = re.findall(r'status=(\d+)', status_line)
    if len(matches) == 1:
        status = int(matches[0])
        try:
            return HTTPStatus(status).value
        except ValueError:
            return HTTPStatus.OK

    return HTTPStatus.OK


def get_status_phrase(status_code):
    """
    Get status phrase by status code
    """
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return HTTPStatus(200).phrase
