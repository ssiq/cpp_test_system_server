import os

from client_utility import post, zip_in_momery, get_csrf_token, download_file, csrf
from utility.constant_value import *
from utility.encrypt import Crypter, RsaCrypter


def create_one_exam(name, begin_time, end_time):
    return post(create_exam_one_url,
                {
                    'name': name,
                    'begin_time': begin_time,
                    'end_time': end_time,
                 },
                [])


def show_exams(json_str):
    import pandas as pd
    print pd.DataFrame(json_str['exams'], columns=['id', 'name', 'begin_time', 'end_time'])


def get_all_exams_list():
    return post(get_exams_list_url,
                {},
                [],
                show_exams)


def get_active_exam_list():
    return post(get_active_exams_url,
                {},
                [],
                show_exams)


def show_it(x):
    import io
    import zipfile
    import itertools
    os.chdir('../')
    crypter = Crypter(loc=key_place)
    input_rsa = RsaCrypter(loc=rsa_input_key_place)
    output_rsa = RsaCrypter(loc=rsa_output_key_place)
    for question in x['question']:
        print 'question:{}'.format(question)
        plain = crypter.decrypt(question)
        out_io_buffer = io.BytesIO()
        with zipfile.ZipFile(out_io_buffer, "a", zipfile.ZIP_DEFLATED, False) as out_zip, \
             zipfile.ZipFile(io.BytesIO(plain)) as in_zip:
            for t in itertools.ifilter(lambda x: not(x.endswith("in") or x.endswith("out")),
                                       in_zip.namelist()):
                out_zip.writestr(t, in_zip.read(t))
            for t in itertools.ifilter(lambda x: x.endswith("in"),
                                       in_zip.namelist()):
                out_zip.writestr(t, input_rsa.decrypt(in_zip.read(t)))
            for t in itertools.ifilter(lambda x: x.endswith("out"),
                                       in_zip.namelist()):
                out_zip.writestr(t, output_rsa.decrypt(in_zip.read(t)))
        with open('dest/q.zip', 'wb') as f:
            f.write(out_io_buffer.getvalue())



def download_one_exam(eid):
    return post(download_total_exam_url, {'eid': eid}, [], show_it)


def upload_score(eid, qlist, score_list):
    return post(upload_exam_score_url, {'eid':eid, 'qid': qlist, 'score': score_list}, [], show_it)


def upload_project(eid, log, prpject, has_monitor=0, has_browser=0, monitor='empty', browser='empty'):
    file_field = {'log':log, 'project':prpject}
    if has_monitor:
        file_field['monitor'] = monitor
    if has_browser:
        file_field['chrome'] = browser
    return post(upload_exam_project_url, {'eid': eid, 'hasMonitor': has_monitor, 'hasChrome': has_browser},
                file_field, show_it)


def upload_project_and_score(eid, qlist, score_list, log, prpject,
                             has_monitor=0, has_browser=0, monitor='empty', browser='empty'):
    file_field = {'log': log, 'project': prpject}
    if has_monitor:
        file_field['monitor'] = monitor
    if has_browser:
        file_field['chrome'] = browser
    return post(upload_exam_project_and_score_url, {'eid':eid, 'qid': qlist, 'score': score_list,
                                                    'hasMonitor': has_monitor, 'hasChrome': has_browser},
                file_field, show_it)


def create_one_question(path):
    import os
    import scandir
    import re
    d = {}
    name_path = path+'/name'
    desc_path = path+'/description'
    test_path = path+'/test_cases'
    if not os.path.isdir(path):
        print 'path %s id not a path' % path
        return False
    if not os.path.isfile(name_path):
        print 'no name'
        return False
    if not os.path.isfile(desc_path):
        print 'no description'
        return False
    if not os.path.isdir(test_path):
        print 'no test cases'
        return False

    in_pattern = re.compile(r'(\w+).in$')
    out_pattern = re.compile(r'(\w+).out$')
    in_list = []
    out_list = []
    for entry in scandir.scandir(test_path):
        name = entry.name
        if not entry.is_file():
            print '%s is not a file' % name
            return False
        match = in_pattern.match(name)
        if match is None:
            match = out_pattern.match(name)
            if match is None:
                print '%s is not in and not out' % name
                return False
            else:
                out_list.append(match.group(1))
        else:
            in_list.append(match.group(1))

    if len(in_list) == 0:
        print '%s contains no test in' % test_path
        return False
    if len(out_list) == 0:
        print '%s contains no test out' % test_path
        return False

    for i in in_list:
        if i not in out_list:
            print 'in file %s doesn\'t have corresponding out file' % i
            return False

    for i in out_list:
        if i not in in_list:
            print 'out file %s doesn\'t have corresponding in file' % i
            return False

    with open(name_path, 'r') as f:
        d['name'] = f.read().replace('\n', '')

    with open(desc_path, 'r') as f:
        d['description'] = f.read()
    files = dict()
    files['content'] = zip_in_momery(path).getvalue()
    return post(create_one_question_url, d, files)


def get_one_question(question_id, dest_path):
    chunk_size = 1024

    def put_file(r):
        import re
        pattern = re.compile(r'.+=(.+)\.zip')
        m = pattern.match(r.headers.get('Content-Disposition'))
        with open(dest_path+'/'+m.group(1)+'.zip', 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
    return post(get_one_question_url,
                data_dict={'id': question_id},
                handle_response=put_file)


def get_exam_quesiton(exam_id, question_id, dest_path):

    def action(x):
        from utility.encrypt import Crypter
        crypter = Crypter('../keys')
        name = x['name']
        question = x['question']
        print question
        question = crypter.decrypt(question)
        with open(dest_path + '/' + name +'.zip', 'wb') as f:
            f.write(question)

    return post(download_exam_quesiton_view_url,
                {
                    'eid': exam_id,
                    'qid': question_id,
                },
                action=action)


def upload_exams(path):
    pass


def change_exam(path):
    pass