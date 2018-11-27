import requests

payload = 'kek.kek'


def check(url):
    """
    Payload found in response
    :param url:
    :return:
    """
    try:
        return True if requests.get(url, headers={'X-Forwarded-Host': payload}).text.find(payload) > -1 else False
    except:
        pass
    return False
