from client.exam_manage import *
from client.user_manage import login


def test_create_one_exam():
    assert create_one_exam('test3', '2016-05-13 19:00:00', '2016-05-13 21:00:00'), 'create one exam error'


def test_get_all_exams_list():
    assert get_all_exams_list(), 'get all exams list error'


def test_get_active_exams_list():
    assert get_active_exam_list(), 'get active list error'


def test_create_one_question():
    assert create_one_question('question1'), 'create one question error'


def test_get_one_question():
    assert get_one_question(10, 'dest'), 'get one question error'
    assert get_one_question(1, 'dest') == False, 'get one question error'


def test_get_exam_question():
    assert get_exam_quesiton('1', '10', 'dest'), 'get exam question error'


def test_download_one_exam():
    assert download_one_exam('1'), 'get one exam error'


def test_upload_score():
    assert upload_score('1', ["10"], ["100"]), 'upload score error'


def test_upload_projects():
    with open('dest/q.zip', 'rb') as f:
        log = f.read()
        project = log
        assert upload_project('1', log, project), 'upload log error'


def test_upload_project_and_score():
    with open('dest/q.zip', 'rb') as f:
        log = f.read()
        project = log
        assert upload_project_and_score('1', ["10"], ["100"], log, project), 'upload score and log error'


if __name__ == '__main__':
    login('stu7', 'stu7')
    # test_create_one_exam()
    # test_get_all_exams_list()
    # test_get_active_exams_list()
    # test_create_one_question()
    # test_get_one_question()
    # test_get_exam_question()
    # test_download_one_exam()
    # test_upload_score()
    # test_upload_projects()
    test_upload_project_and_score()
