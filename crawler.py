from html.parser import HTMLParser
from urllib import parse

import requests


class LinkParser(HTMLParser):

    same_domain = False
    blocked_list = ['.png', '.jpg', '.svg', '.css']

    def handle_starttag(self, tag, attrs):
        """
        Need for HTMLParser params
        :param tag:
        :param attrs:
        :return:
        """
        if tag == 'a' or tag == 'link':
            for (key, value) in attrs:
                if key == 'href' and not any(ext in value for ext in self.blocked_list):
                    if self.same_domain:
                        # check that value is another domain
                        if 'http://' in value or 'https://' in value:
                            # check domain. same or another
                            if str(self.baseUrl).replace('http://', '').replace('https://', '') in value:
                                self.links = self.links + [parse.urljoin(self.baseUrl, value)]
                        # check that value do not contains any scheme
                        if not '://' in value:
                            self.links = self.links + [parse.urljoin(self.baseUrl, value)]
                    if not self.same_domain:
                        self.links = self.links + [parse.urljoin(self.baseUrl, value)]

        if tag == 'img' or tag == 'script':
            for (key, value) in attrs:
                if key == 'src' and not any(ext in value for ext in self.blocked_list):
                    if self.same_domain:
                        # check that value is another domain
                        if 'http://' in value or 'https://' in value:
                            # check domain. same or another
                            if str(self.baseUrl).replace('http://', '').replace('https://', '') in value:
                                self.links = self.links + [parse.urljoin(self.baseUrl, value)]
                        # check that value do not contains any scheme
                        if not '://' in value:
                            self.links = self.links + [parse.urljoin(self.baseUrl, value)]
                    if not self.same_domain:
                        self.links = self.links + [parse.urljoin(self.baseUrl, value)]

    def getLinks(self, url):
        """
        Parse html and get links from rules, described in handle_starttag()
        :param url:
        :return:
        """
        self.links = []
        self.baseUrl = url
        requests.packages.urllib3.disable_warnings()
        return HTMLParser.feed(self, requests.get(url, timeout=4, verify=False).text), self.links


def spider(url, maxPages=20, same_domain=True):
    """
    Do all magic here
    :param url:
    :param maxPages:
    :return:
    """
    LinkParser.same_domain = same_domain
    pagesToVisit = [url]
    numberVisited = 0
    links = []
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
            links = set(links)
        except Exception as ex:
            pass #print(ex)
    return links if len(links) > 0 else [url]
