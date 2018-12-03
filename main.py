import config
import scan

# need crawl or just test some url's
no_need_to_crawl = False

start_url = ''

# fill list of sites instead of start_url if you want a list
urlList = [
    'https://site1.com',
    'site2.com.cy'
]

# uncomment what you need
scan_options = [
    config.WEB_CACHE_DECEPTION,
    config.CRLF,
    config.REVERSE_TABNABBING
]


def do_magic():
    if start_url == '' and len(urlList) == 0:
        print('Check your targets')
    else:
        if start_url != '':
            scan.crawl_and_scan(start_url, scan_options)
        if len(urlList) > 0:
            for url in urlList:
                print('Now scan ' + url)
                scan.scan(url, scan_options) if no_need_to_crawl else scan.crawl_and_scan(url, scan_options)


if __name__ == '__main__':
    do_magic()
