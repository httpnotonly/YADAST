# x-forwarded-for
# https://www.whitehatsec.com/blog/top-3-proxy-issues-that-no-one-ever-told-you/
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
            'X-Forwarded-Host': '127.0.0.1'
        }),
        cookies = old_cookies
    )
    if new_response.status_code != old_response.status_code or len(new_response.text) != len(old_response.text):
        return new_response
    return False
