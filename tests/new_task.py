from pprint import pprint

import requests

from run import new_task

target = 'site.com'
need_crawl = True

message = {
    'data': {
        'target': target,
        'need_crawl': need_crawl,
        'wcd': True,
        'trace': True
    }
}

pprint(new_task(message))
pprint('scan done')
