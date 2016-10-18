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
        eid = int(eid.split('/')[0])
        exam = Exam.objects.get(id=eid)

        questions = ExamQuestion.objects.filter(exam=exam)
        question_weights = {}
        weight_sum = 0.0
        for q in questions:
            question_weights[q.question_id] = q.percent
            weight_sum += q.percent

        scores = Score.objects.filter(exam=exam)
        student_dict = {}
        for score in scores:
            if score.user.username not in student_dict:
                student_dict[score.user.username] = {}
            if score.question_id in student_dict[score.user.username]:
                student_dict[score.user.username][score.question_id] = max(score.score,
                                                                           student_dict[score.user.username][
                                                                               score.question_id])
            else:
                student_dict[score.user.username][score.question_id] = score.score

        score_dict = {}
        for username, d in student_dict.items():
            s = 0.0
            for k, v in d.items():
                s += float(question_weights[k]) * v
            s /= float(weight_sum)
            score_dict[username] = s

        dataframe = pd.DataFrame({
            'student_id': score_dict.keys(),
            'score': score_dict.values(),
        })

        f = StringIO()
        dataframe.to_csv(f)
        response = HttpResponse(f.getvalue(), content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=%s_student_score.csv' % exam.name
        return response


@admin.register(ExamRandomMd5)
class ExamRandomMd5Admin(admin.ModelAdmin):
    search_fields = ['user__username', ]
    readonly_fields = ('exam', 'user', 'md5')
