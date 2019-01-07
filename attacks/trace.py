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
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        return True if http.request('TRACE', url).status != 405 else False
    except Exception as ex:
        pprint(ex)
    return False
