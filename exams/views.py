# -*- coding: utf-8 -*-
from wsgiref.util import FileWrapper

from django.http import JsonResponse
from django.contrib.auth.models import User
from utility.constant_value import ok_result, random_code
from utility.utility_funciton import strptime
from utility.utility_funciton import generate_error_response
from utility.decorator import *
from utility.encrypt import Crypter
from models import *
from django.utils import timezone
from django.http import HttpResponse
from cStringIO import StringIO

from utility.constant_value import key_place
# Create your views here.


@check_login
@check_permission
@catch_exception
def create_exam_view(request):
    name = request.POST['name']
    begin_time = request.POST['begin_time']
    end_time = request.POST['end_time']
    exam = Exam.objects.create(name=name, begin_time=strptime(begin_time), end_time=strptime(end_time))
    exam.save()
    return JsonResponse(ok_result)


def change_time_zone(t):
    import pytz
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    return timezone.localtime(t)


def exams_to_dict(exams):
    d = {
        'id': [],
        'name': [],
        'begin_time': [],
        'end_time': [],
        'is_homework': [],
    }
    for exam in exams:
        d['id'].append(exam.id)
        d['name'].append(exam.name)
        d['begin_time'].append(change_time_zone(exam.begin_time))
        d['end_time'].append(change_time_zone(exam.end_time))
        d['is_homework'].append(exam.isHomework)
    return d


@check_login
@check_permission
@catch_exception
def get_exam_list_view(request):
    all_exams = Exam.objects.all()
    r = {'exams': exams_to_dict(all_exams)}
    r.update(ok_result)
    return JsonResponse(r)


@check_login
@catch_exception
def get_active_exam_list_view(request):
    now = timezone.now()
    active_exams = Exam.objects.filter(end_time__gt=now, begin_time__lt=now)
    r = {'exams': exams_to_dict(active_exams)}
    r.update(ok_result)
    return JsonResponse(r)


@check_login
@catch_exception
def get_one_exam_view(request):
    pass


@check_login
@check_permission
@catch_exception
def create_question_view(request):
    name = request.POST['name']
    description = request.POST['description']
    content = request.FILES['content']
    question = Question.objects.create(name=name, description=description, content=content)
    question.save()
    return JsonResponse(ok_result)


@check_login
@check_permission
@catch_exception
def get_question_list_view(request):
    questions = Question.objects.all()
    d = {
        'id': [],
        'name': [],
        'description': [],
    }
    for question in questions:
        d['id'] = question.id
        d['name'] = question.name
        d['description'] = question.description
    r = {'questions': d}
    r.update(ok_result)
    return JsonResponse(r)


@check_login
@check_permission
def change_question_view(request):
    pass


@check_login
@check_permission
@catch_exception
def get_question_view(request):
    qid = request.POST['id']
    question = Question.objects.get(id=qid)
    name = question.name
    f = question.content
    f.open('rb')
    response = HttpResponse(FileWrapper(f), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % name
    return response


def _check(exam):
    now = timezone.now()
    s = 'homework' if exam.isHomework else 'exam'
    if exam.begin_time > now:
        raise Exception('this %s does not begin' % s)
    elif exam.end_time < now:
        raise Exception('this %s has ended' % s)


def _check_random_code(exam, request):
    if not exam.isHomework:
        er_list = ExamRandomMd5.objects.filter(user=request.user, exam=exam)
        if er_list is None or len(er_list) == 0:
            er = ExamRandomMd5.objects.create(user=request.user, exam=exam, md5=request.session[random_code])
            er.save()
        else:
            er = er_list[0]
            if er.md5 != request.session[random_code]:
                raise Exception(u'you can not login one exam twice')


@check_login
@catch_exception
def download_exam_question_view(request):
    eid = request.POST['eid']
    qid = request.POST['qid']
    exam = Exam.objects.get(id=eid)
    _check(exam)
    _check_random_code(exam, request)
    question = Question.objects.get(id=qid)
    l = ExamQuestion.objects.filter(exam=exam, question=question)
    if l is None or len(l) != 1:
        s = 'homework' if exam.isHomework else 'exam'
        raise Exception('this question is not in the %s' % s)
    crypter = Crypter(loc='keys')
    content = question.content
    content.open('rb')
    v = crypter.encrypt(content.read())
    print v
    res = {'question': v, 'name': question.name}
    res.update(ok_result)
    return JsonResponse(res)


@check_login
@catch_exception
def download_total_exam(request):
    eid = request.POST['eid']
    exam = Exam.objects.get(id=eid)
    _check(exam)
    _check_random_code(exam, request)
    questions = ExamQuestion.objects.filter(exam=exam)
    crypter = Crypter(loc=key_place)
    question_list = []
    name_list = []
    question_id_list = []
    for question in questions:
        # print question
        question.question.content.open('rb')
        question_list.append(crypter.encrypt(question.question.content.read()))
        name_list.append(question.question.name)
        # print type(question.question_id)
        question_id_list.append(question.question_id)
    res = {'question': question_list, 'name': name_list, 'question_id': question_id_list}
    res.update(ok_result)
    print res
    return JsonResponse(res)


def save_score(request, exam):
    import json
    qid_list = json.loads(request.POST['qid'])
    score_list = json.loads(request.POST['score'])
    if not isinstance(qid_list, list):
        question = Question.objects.get(id=qid_list)
        score_obj = Score.objects.create(question=question, exam=exam, user=request.user, score=score_list)
        score_obj.save()
    else:
        for qid, score in zip(qid_list, score_list):
            print 'qid:{}, score:{}'.format(qid, score)
            question = Question.objects.get(id=qid)
            score_obj = Score.objects.create(question=question, exam=exam, user=request.user, score=score)
            score_obj.save()
    return True


@check_login
@catch_exception
def upload_exam_score_view(request):
    # print request.POST
    # print request.body
    eid = request.POST['eid']
    # print 'eid:{}'.format(eid)
    exam = Exam.objects.get(id=eid)
    _check(exam)
    _check_random_code(exam, request)
    # print 'all check passed'
    save_score(request, exam)
    return JsonResponse(ok_result)


def save_log_project(request, exam):
    log_file = request.FILES['log']
    project_file = request.FILES['project']
    # ep_list = ExamProjects.objects.filter(user=request.user, exam=exam)
    # if ep_list is None or len(ep_list) == 0:
    ep = ExamProjects.objects.create(user=request.user, exam=exam)
    # else:
    #     ep = ep_list[0]
    ep.log = log_file
    ep.project = project_file
    ep.save()


@check_login
@catch_exception
def upload_exam_log_project(request):
    eid = request.POST['eid']
    exam = Exam.objects.get(id=eid)
    _check(exam)
    _check_random_code(exam, request)
    save_log_project(request, exam)
    return JsonResponse(ok_result)


@check_login
@catch_exception
def upload_exam_log_project_score(request):
    eid = request.POST['eid']
    exam = Exam.objects.get(id=eid)
    _check(exam)
    _check_random_code(exam, request)
    save_score(request, exam)
    save_log_project(request, exam)
    return JsonResponse(ok_result)
