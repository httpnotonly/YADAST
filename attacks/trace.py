from pprint import pprint
from attacks.bypasses import xff, waf
import requests


# TODO refactoring with functional programming
def check(url):
    """
    Payload found in response
    :param url:
    :return:
    """
    try:
        response = requests.request('TRACE', url, verify=False)
        if response.status_code != 405 and not waf.detect_waf(response.text):
            return True
        else:
            bypassed_response = xff.xff(response, 'TRACE')
            if bypassed_response:
                if bypassed_response.status_code != 405 and not waf.detect_waf(bypassed_response.text):
                    pprint('BYPASS is detected')
                    return True
        return False
    except Exception as ex:
        pprint(ex)
    return False
