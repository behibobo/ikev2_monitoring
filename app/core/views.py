
from flask import Blueprint, current_app, jsonify
from werkzeug.local import LocalProxy
import psutil
import os
from authentication import require_appkey

core = Blueprint('core', __name__)
logger = LocalProxy(lambda: current_app.logger)


@core.before_request
def before_request_func():
    current_app.logger.name = 'core'



@core.route('/system_information', methods=['GET'])
# @require_appkey
def system_information():
    virtual_memory = psutil.virtual_memory()
    net_io = psutil.net_io_counters()

    data = {
        'memory': {
            'total': bytes_to_GB(virtual_memory.total),
            'available': bytes_to_GB(virtual_memory.available),
            'used': bytes_to_GB(virtual_memory.used),
            'percentage': psutil.cpu_percent(),
        },
        'cpu': {
            'usage': psutil.cpu_percent()
        },
        'network': {
            'sent': bytes_to_GB(net_io.bytes_sent),
            'received': bytes_to_GB(net_io.bytes_recv)
        }
        
    }
    return jsonify(data)

@core.route('/ikev_users', methods=['GET'])
# @require_appkey
def ikev_users():
    stream = os.popen('strongswan leases | head -n 1')
    res = stream.read()
    arr = res.split(",")[1:]
    data = {
        'Total Users':  arr[0][arr[0].find("/")-1],
        'Online Users': arr[1].strip()[:1]
    }
    return jsonify(data)


def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb