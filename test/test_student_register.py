from client.user_manage import *


def test_upload_stu_information():
    assert upload_stu_information('student_list'), 'upload student error'


def test_one_student_register():
    assert register_student('stu5', 'stu5'), 'register student error'


if __name__ == '__main__':
    # test_upload_stu_information()
    test_one_student_register()
