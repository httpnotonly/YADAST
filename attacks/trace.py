from pprint import pprint
import urllib3

payload = 'TRACE'


def check(url):
    """
    Payload found in response
    :param url:
    :return:
    """
    try:
        http = urllib3.PoolManager()
        return True if http.request('TRACE', url).status != 405 else False
    except Exception as ex:
        pprint(ex)
    return False
