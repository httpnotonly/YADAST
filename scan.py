from pprint import pprint

import requests

import config
import crawler
from attacks import WebCacheDeception, crlf, ReverseTabnabbing


def scan(url, options=[]):
    """
    Scan crawled urls
    :param url:
    :param options:
    :return:
    """
    if len(options) == 0:
        print('Check your scan options')
        return False
    else:
        if config.WEB_CACHE_DECEPTION in options:
            if WebCacheDeception.check(url):
                print(url + ' is vulnerable to ' + config.WEB_CACHE_DECEPTION)
        if config.CRLF in options:
            if crlf.check(url):
                print(url + ' is vulnerable to ' + config.CRLF)
        if config.REVERSE_TABNABBING in options:
            if ReverseTabnabbing.check(url):
                print(url + ' is vulnerable to ' + config.REVERSE_TABNABBING)
    return True


def crawl_and_scan(start_url, options=[]):
    """
    To making magic without brain job
    :param start_url:
    :param options:
    :return:
    """
    start_url = url_prepare(start_url)
    sitemap = crawler.spider(start_url)
    if len(sitemap) > 0:
        print(str(len(sitemap)) + ' urls detected')
        for url in sitemap:
            scan(url, options)
        return True
    return False


def url_prepare(url):
    """
    If url does't contains http scheme
    :param url:
    :return:
    """
    if 'http://' in url or 'https://' in url:
        return url
    try:
        if requests.get('https://' + url):
            return 'https://' + url
    except:
        pass
        # no https
    return 'http://' + url