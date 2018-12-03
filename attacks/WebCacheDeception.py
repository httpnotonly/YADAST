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
            return True if requests.get(url, headers={'X-Forwarded-Host': payload}).text.find(payload) > -1 else False
        if xss:
            return True if requests.get(url, headers={'X-Forwarded-Host': xss_payload}).text.find(
                xss_payload) > -1 else False
    except:
        pass
    return False
