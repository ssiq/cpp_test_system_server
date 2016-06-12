import json

from config import server_ip
from utility.utility_funciton import is_ok

csrf = 'csrfmiddlewaretoken'


def generate_url(sub_path):
    s = r'/'.join(sub_path)
    return server_ip + r'/' + s + r'/'


class Token(object):
    session = None

    @staticmethod
    def get_csrf_token():
        import requests
        # response = requests.get(generate_url(['get_csrf']))
        if Token.session is None:
            s = requests.Session()
            Token.session = s
        else:
            s = Token.session
        response = s.get(generate_url(['get_csrf']))
        # print response.cookies
        return s, response.cookies['csrftoken']


def get_csrf_token():
    return Token.get_csrf_token()


def generate_return(response, action=(lambda x: None), handle_response=(lambda x: None)):
    response.raise_for_status()
    if response.headers.get('content-type').lower() != 'application/json':
        handle_response(response)
        return True
    else:
        json_str = json.loads(response.text)
        if is_ok(json_str):
            action(json_str)
            return True
        else:
            print json_str['msg']
            return False


def post(url, data_dict=dict(), files_list=list(), action=(lambda x: None), handle_response=(lambda x: None)):
    session, token = get_csrf_token()
    d_dict = {csrf: token}
    d_dict.update(data_dict)
    response = session.post(generate_url([url]),
                            data=d_dict, files=files_list)
    return generate_return(response, action, handle_response)


def download_file(url, dest):
    session, token = get_csrf_token()
    d_dict = {csrf: token}
    response = session.post(generate_url(['download', url]), data=d_dict)
    if response.status_code != 200:
        print 'download file failed'
        return
    q = response.raw.read()
    response
    with open(dest, 'w') as f:
        f.write(q)


def zip_in_momery(src):
    from cStringIO import StringIO
    import zipfile
    import os
    stringIO = StringIO()
    zf = zipfile.ZipFile(stringIO, "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()
    return stringIO
