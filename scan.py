from pprint import pprint

import requests

import config
import crawler
from attacks import WebCacheDeception, crlf, ReverseTabnabbing, trace


def scan(url, options=[]):
    """
    Scan crawled urls
    :param url:
    :param options:
    :return:
    """
    findings = []
    url = url_prepare(url)
    if len(options) == 0:
        print('Check your scan options')
        return False
    else:
        if config.WEB_CACHE_DECEPTION in options:
            if WebCacheDeception.check(url):
                print(url + ' is vulnerable to ' + config.WEB_CACHE_DECEPTION)
                findings.append(config.WEB_CACHE_DECEPTION)
                if WebCacheDeception.check(url, xss=True):
                    print(url + ' is also vulnerable to ' + config.XSS + ' via ' + config.WEB_CACHE_DECEPTION)
                    findings.append(config.XSS + '_' + config.WEB_CACHE_DECEPTION)
        if config.CRLF in options:
            if crlf.check(url):
                print(url + ' is vulnerable to ' + config.CRLF)
                findings.append(config.CRLF)
        if config.TRACE in options:
            if trace.check(url):
                print(url + ' is vulnerable to ' + config.TRACE)
                findings.append(config.TRACE)
        if config.REVERSE_TABNABBING in options:
            if ReverseTabnabbing.check(url):
                print(url + ' is vulnerable to ' + config.REVERSE_TABNABBING)
                findings.append(config.REVERSE_TABNABBING)

    return findings


def crawl_and_scan(start_url, options=[], same_domain=True):
    """
    Crawl first and then scan
    :param start_url:
    :param options:
    :param same_domain:
    :return:
    """
    vulns = {}
    start_url = url_prepare(start_url)
    sitemap = crawler.spider(start_url, same_domain=same_domain)
    if len(sitemap) > 0:
        print(str(len(sitemap)) + ' urls detected')
        for url in sitemap:
            # progress logging
            print(str(list(sitemap).index(url)) + '/' + str(len(sitemap)) + ' ' + url)
            vulns[url] = scan(url, options)
        return vulns
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
    except Exception as ex:
        pprint(ex)
    return 'http://' + url
