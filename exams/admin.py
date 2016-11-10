# -*- coding: utf-8 -*-
from wsgiref.util import FileWrapper

from django import forms
from django.conf.urls import patterns
from django.contrib import admin
from django.http import HttpResponse

from models import *
# Register your models here.


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1


class ScoreInline(admin.TabularInline):
    model = Score
    readonly_fields = ('user', 'question', 'score')
    can_delete = False
    extra = 0


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        import re
        content = self.cleaned_data.get('content')
        question_directory_pattern = re.compile(r'[^/]+/question/')
        test_cases_directory_pattern = re.compile(r'[^/]+/test_cases/')
        try:
            content.open('rb')
            f = zipfile.ZipFile(content, 'r')
        except Exception, e:
            print e
            raise forms.ValidationError(u"你上传内容文件不是一个zip包")
        question_direcory_exist = False
        test_cases_directory_exist = False
        for name in f.namelist():
            if question_directory_pattern.match(name) is not None:
                question_direcory_exist = True
            if test_cases_directory_pattern.match(name) is not None:
                test_cases_directory_exist = True

        if question_direcory_exist and test_cases_directory_exist:
            pass
        else:
            s = u""
            if not question_direcory_exist:
                s += u"question子文件夹"
            if not test_cases_directory_exist:
                if s != u"":
                    s += u'和'
                s += u"test_cases子文件夹"
            raise forms.ValidationError(u"你提交的zip文件包不包含{}".format(s))
        return super(QuestionForm, self).clean()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', )
    list_display = ['name', 'id']
    fieldsets = [(
                    None, {
                        'fields': ['name', 'description', 'content'],
                        'description': u'提交的文件内容应该是一个zip包,里面有两个文件夹,test_cases和question',
                    }
    )]
    form = QuestionForm


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    change_form_template = 'admin/exams/exam_change_form.html'
    list_display = ['name', 'begin_time', 'end_time']
    inlines = (ExamQuestionInline, )

    def get_urls(self):
        urls = super(ExamAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^(.+)/download_scores/$', self.admin_site.admin_view(self.download_scores)),
                           )
        return my_urls + urls

    def download_scores(self, request, eid):
        import pandas as pd
        from cStringIO import StringIO
        from django.db import connection
        import MySQLdb
        from collections import deque
        # db = MySQLdb.connect("localhost", "ana", "anapassword", "cpp_test_server")
        eid = int(eid.split('/')[0])
        exam = Exam.objects.get(id=eid)

        grade_df = pd.read_sql(
            'select max(score) as score, u.username, s.question_id from auth_user u, exams_score s where u.id = s.user_id and s.exam_id ={} group by s.question_id, u.username'.format(eid),
            con=connection)
        # f = StringIO()
        response = HttpResponse(content_type='application/csv')
        # response['Content-Disposition'] = 'attachment;filename="%s_student_score.csv"' % exam.name
        response['Content-Disposition'] = 'filename="%s_student_score.csv"' % exam.name
        grade_df.to_csv(response)
        print response['Content-Disposition']
        return response


@admin.register(ExamRandomMd5)
class ExamRandomMd5Admin(admin.ModelAdmin):
    search_fields = ['=user__username', ]
    readonly_fields = ('exam', 'user', 'md5')


@admin.register(ExamProjects)
class ExamProjectsAdmin(admin.ModelAdmin):
    search_fields = ['=user__username', '=exam__id']
    readonly_fields = ('exam', 'user', 'log', 'project', 'create_time')
    list_display = ['exam', 'user', 'create_time']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    search_fields = ['=user__username', '=exam__id', '=question__id']
    list_display = ['exam', 'user', 'question', 'score']
    readonly_fields = ('exam', 'user',  'question', 'score',)


@admin.register(ExamMac)
class ExamMacAdmin(admin.ModelAdmin):
    search_fields = ['=user__username', '=exam__id']
    list_display = ['exam', 'user', 'mac']
    readonly_fields = ('exam', 'user', 'mac')

