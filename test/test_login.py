from client.user_manage import *


def test_login():
    def a(s):
        print s

    login('stu7', 'stu7', '0bb39f9eae5cc10d03e3b1b0e02839b2', action=a)


if __name__ == '__main__':
    test_login()
