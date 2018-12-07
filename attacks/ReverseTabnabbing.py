from pprint import pprint

import requests

import config

payload = '_blank'
fixes = ['noopener', 'noreferrer', 'nofollow']


def check(url):
    """
    Payload found in response
    :param url:
    :return:
    """
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.get(url, verify=False)
        if response.text.find(payload) > -1:
            print('Possible ' + config.REVERSE_TABNABBING + ' is here ' + url)
            for fix_word in fixes:
                if response.text.find(fix_word) > -1:
                    return False
            return True
    except Exception as ex:
        pprint(ex)
    return False
