import requests
import json
from utility.utility_funciton import is_ok
from utility.constant_value import *
from client_utility import generate_url, get_csrf_token, csrf, generate_return, post


def upload_stu_information(path):
    session, token = get_csrf_token()
    print token
    response = session.post(generate_url(['register', 'students']),
                            files=[('student_list', open(path, 'rb'))],
                            data={csrf: token})
    return is_ok(json.loads(response.text))


def register_student(sid, password):
    session, token = get_csrf_token()
    response = session.post(generate_url(['register', 'one_student']),
                            data={csrf: token, 'sid': sid, 'password': password})
    return generate_return(response)


def login(username, password):
    return post(login_url, {'username': username, 'password': password}, [])
