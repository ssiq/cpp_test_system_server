from wsgiref.util import FileWrapper

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


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', )


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
        for q in questions:
            question_weights[q.question_id] = q.percent

        scores = Score.objects.filter(exam=exam)
        student_dict = {}
        for score in scores:
            if score.user.username not in student_dict:
                student_dict[score.user.username] = 0.0
            student_dict[score.user.username] += float(question_weights[score.question_id]) * score.score

        dataframe = pd.DataFrame({
            'student_id': student_dict.keys(),
            'score': student_dict.values(),
        })

        f = StringIO()
        dataframe.to_csv(f)
        response = HttpResponse(f.getvalue(), content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=%s_student_score.csv' % exam.name
        return response


@admin.register(ExamRandomMd5)
class ExamRandomMd5Admin(admin.ModelAdmin):
    pass
