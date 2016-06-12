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
* /login 登陆
    输入Post:
    {
        'username': ,
        'password': ,
    }
* /logout 注销
* /exams/get_active_list 获得正在进行的考试和作业 
    如果没有错误发生.返回:
    {
        'result':'ok',
        'id': list,
        'name': list,
        'begin_time': list,
        'end_time': list,
        'is_homework': list,
    }
