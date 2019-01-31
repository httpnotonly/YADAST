from pprint import pprint
from run import new_task

target = 'site.com'
need_crawl = True
same_domain = False

message = {
    'data': {
        'target': target,
        'need_crawl': need_crawl,
        'same_domain': same_domain,
        'wcd': True,
        'trace': False,
        'crlf': False,
        'reverse_tabnabbing': False
    }
}

pprint(new_task(message))
pprint('scan done')
