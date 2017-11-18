# 功能点
1. 注册,登陆(OK)
2. 上传考试数据(OK)
3. 学生客户端下载考试数据
4. 上传考试结果
5. 上传考试log
6. 助教获得考试结果(OK)

# return json
if ok
{
    'result':'ok'
    something else
}

if some error happened
{
    'result':'error'
    'msg': error message
}


# client api
* /get_csrf
    没有返回json
    cookie中会有'csrftoken':token
    每次上传时POST中都要有'csrfmiddlewaretoken': token
    
* /check_version 告诉服务器插件的版本
    在Post参数中
    {
        'version': ,
    }
    在get_csrf之后应该立刻调用这个方法
    
* /login 登陆
    input:
    {
        'username': ,
        'password': ,
        'used_key': ,
    }
    输出:
    {
        'new_login': ,#False means that the user's last login is not logout
        'used_key': ,#the used key to update
    }
* /logout 注销
* /exams/get_active_list 获得正在进行的考试和作业 
    如果没有错误发生.返回:
    {
        'result':'ok',
        'exams':{
                    'id': list,
                    'name': list,
                    'begin_time': list,
                    'end_time': list,
                    'is_homework': list,
                }
    }

* /exam/download_total/  获取整个考试
    input:
    {
        'eid': , #the exam id
    }
    return:
    the ok_result and
    {
        'question': question_list, # the question content list
        'name': name_list # the question name list
    }

    The question_list is an encrypted zip file

* /exam/upload_score/  上传考试分数
    input:
    {
        'eid': # exam id
        'qid': # the list of question id in the exam which should be a json list
        'score': # the score list of the corresponding question which should be a json list
    }
    return:
    the ok_result

* /exam/upload_exam_log_project/  上传考试工程和log 
    input:
    {
        'eid': # exam id,
        'log': # the log file of the exam, use FILE upload
        'project': # the zipped project files, use FILE upload
    }
    return:
    ok_result

* /exam/upload_exam_project_and_score/ 同事上传工程,log和成绩
    input:
    {
        'eid': # exam id
        'qid': # the list of question id in the exam which should be a json list
        'score': # the score list of the corresponding question which should be a json list
        'log': # the log file of the exam, use FILE upload
        'project': # the zipped project files, use FILE upload
    }
    return:
    the ok_result

# the upload question format
in the question zip file:
    |question # this directory contains question description
    |test_cases # this directory contains test data
in the test directory every test data has a *.in and *.out file, they have the same name but the different suffix
    
# deploy

1. sudo apt-get install apache2 libapache2-mod-wsgi
2. edit the files in apache file to change the path of the project
3. copy the cpp_test_system_server.conf file in apache directory to /etc/apache2/sites-available
   copy the apache2.conf in apache file to /etc/apache2


# Config

- Update path in `cpp_test_system_server/settings.py`
- Update path in `utility/constant_value.py`
- For test: update url in `client/config.py` 
- install python2.7
- install django
```
conda install django=1.9.9
# pip location should match your python
pip install django==1.9.9
```
- install mysql-python using conda
```
conda install MySQL-python
```
- install mysql
- create user & grant privilege
```
create user 'cpp_test'@'localhost' identified by 'cpp_test';
GRANT ALL PRIVILEGES ON * . * TO 'cpp_test'@'localhost';
```
- create database (had better set mysql server default charset to utf8mb4)
```
CREATE DATABASE cpp_test_server CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```
- install keyczar using pip -- the same pip binary correspond to your python2.7
```
pip install python-keyczar
```
- migrate
```
python2.7 manage.py makemigrations
python2.7 manage.py migrate
```