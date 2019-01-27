import scan


def do_magic(target='', targets=[], need_crawl=False, same_domain=True, what_to_scan=[]):
    """
    scan controller
    :param target:
    :param targets:
    :param need_crawl:
    :param same_domain:
    :param what_to_scan:
    :return:
    """
    vulns = []
    if target == '' and len(targets) == 0:
        print('Check your targets')
    else:
        if target != '':
            print('Now scan ' + target)
            vulns = scan.scan(target, what_to_scan) if not need_crawl else scan.crawl_and_scan(target, what_to_scan, same_domain=same_domain)
        if len(targets) > 0:
            for url in targets:
                print('Now scan ' + url)
                vulns = scan.scan(url, what_to_scan) if not need_crawl else scan.crawl_and_scan(url, what_to_scan, same_domain=same_domain)
    return vulns
