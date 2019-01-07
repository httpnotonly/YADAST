from pprint import pprint

from flask import Flask
from flask_socketio import SocketIO, emit

import config
from main import do_magic

jobs = []
app = Flask(__name__)
app.config['SECRET_KEY'] = 'not_secret_in_code'
socketio = SocketIO(app)


@app.route('/')
def index():
    return 'WebSocket please'


@socketio.on('task')
def new_task(message):
    """
    Message handler
    :param message:
    :return:
    """
    out = []
    try:
        client_request = message['data']
        target = ''
        targets = []
        need_crawl = False
        what_to_scan = []

        if 'target' in client_request:
            target = client_request['target']
        if 'targets' in client_request:
            targets = client_request['targets']
        if 'need_crawl' in client_request:
            need_crawl = bool(client_request['need_crawl'])
        if 'wcd' in client_request:
            if client_request['wcd']:
                what_to_scan.append(config.WEB_CACHE_DECEPTION)
        if 'reverse_tabnabbing' in client_request:
            if client_request['reverse_tabnabbing']:
                what_to_scan.append(config.REVERSE_TABNABBING)
        if 'crlf' in client_request:
            if client_request['crlf']:
                what_to_scan.append(config.CRLF)
        if 'trace' in client_request:
            if client_request['trace']:
                what_to_scan.append(config.TRACE)

        out = do_magic(target, targets, need_crawl, what_to_scan)
        if isinstance(out, dict):
            if len(out.keys()) == 0:
                emit('task', 'nothing found')
                print('nothing found')
            else:
                for key in out:
                    if len(out[key]) > 0:
                        emit('task', key + ' - ' + str(out[key]))
        if isinstance(out, list):
            if len(out) == 0:
                emit('task', 'nothing found')
                print('nothing found')
            else:
                emit('task', str(out))
    except Exception as ex:
        pprint(ex)
    return out


if __name__ == '__main__':
    socketio.run(app)
