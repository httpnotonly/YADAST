
def detect_waf(text):
    """
    Search waf from response body
    :param text:
    :return: True or False
    """
    waf_words = ['Incapsula', 'cloudflare', 'mod_security']
    return True if any(waf in text for waf in waf_words) else False
