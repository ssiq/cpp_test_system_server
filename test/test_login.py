from client.user_manage import *


def test_login():
    def a(s):
        print s

    login('stu7', 'stu7', None, action=a)


if __name__ == '__main__':
    test_login()
