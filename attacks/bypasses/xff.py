# x-forwarded-for
# https://www.whitehatsec.com/blog/top-3-proxy-issues-that-no-one-ever-told-you/
from pprint import pprint

import requests


def xff(old_response, method='GET'):
    """
    X-Forwarded-For technique
    :param old_response:
    :param method:
    :return:
    """
    request = old_response.request
    #FIXME
    old_cookies = {}
    new_response = requests.request(
        method = method,
        url = request.url,
        headers = request.headers.update({
            'X-Forwarded-For': '127.0.0.1',
            'X-Forwarded-Host': '127.0.0.1',
            'X-Real-IP': '127.0.0.1',
            # according to https://tools.ietf.org/html/rfc7239#section-7.4
            'Forwarded': 'for=127.0.0.1;host=127.0.0.1',
        }),
        cookies = old_cookies
    )
    if new_response.status_code != old_response.status_code or len(new_response.text) != len(old_response.text):
        pprint('XFF bypass works')
        return new_response
    return False
