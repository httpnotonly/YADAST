import scan


def do_magic(target='', targets=[], need_crawl=False, what_to_scan=[]):
    """
    scan logic is here
    :param target:
    :param targets:
    :param need_crawl:
    :param what_to_scan:
    :return:
    """
    vulns = []
    if target == '' and len(targets) == 0:
        print('Check your targets')
    else:
        if target != '':
            print('Now scan ' + target)
            vulns = scan.scan(target, what_to_scan) if not need_crawl else scan.crawl_and_scan(target, what_to_scan)
        if len(targets) > 0:
            for url in targets:
                print('Now scan ' + url)
                vulns = scan.scan(url, what_to_scan) if not need_crawl else scan.crawl_and_scan(url, what_to_scan)
    return vulns
