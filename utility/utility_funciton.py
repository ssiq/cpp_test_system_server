from constant_value import *
from django.utils import timezone



def is_ok(r):
    if r['result'] == ok_result['result']:
        return True
    else:
        return False


def generate_error_response(msg):
    r = {
        'msg': msg,
    }
    r.update(error_result)
    return r


__time_format__ = r'%Y-%m-%d %H:%M:%S'


def strptime(s):
    return timezone.datetime.strptime(s, __time_format__)


def strftime(d):
    return d.strftime(__time_format__)


def show_time_format():
    print 'pleas input time as the format %s' % __time_format__


def random_md5_hash():
    import random
    return '%032x' % random.getrandbits(128)
