# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
from django.utils.html import escape
import zipfile


class Exam(models.Model):
    name = models.CharField('exam\'s name', unique=True, max_length=200)
    begin_time = models.DateTimeField('exam\'s begin time')
    end_time = models.DateTimeField('exam\'s end time')
    isHomework = models.BooleanField('is homework?', default=False)
    isPrivate = models.BooleanField('is private?', default=False)

    def show_problems(self):
        problems = ExamQuestion.objects.filter(exam=self)
        html = u'<tr>'

    def __unicode__(self):
        return 'Exam: ' + self.name

    class Meta:
        verbose_name = u'考试'
        verbose_name_plural = verbose_name
        ordering = ['-begin_time']


class Question(models.Model):
    name = models.CharField('question name', unique=True, max_length=200)
    description = models.TextField('question description')
    content = models.FileField('question content', upload_to='uploads/%Y/%m/%d/')
    create_time = models.DateTimeField('create time', default=timezone.now())

    def question_link(self):
        return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)), escape(self.user))

    def __unicode__(self):
        return 'Question: ' + self.name

    class Meta:
        verbose_name = u'题目'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_time = timezone.now()
        return super(Question, self).save(*args, **kwargs)


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    percent = models.IntegerField(verbose_name='question weights in this exam')


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    score = models.FloatField('score')


class ExamRandomMd5(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    md5 = models.CharField(max_length=128, verbose_name='md5')


class ExamProjects(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    log = models.FileField('exam log', upload_to='uploads/log/%Y/%m/%d/')
    project = models.FileField('exam project', upload_to='uploads/project/%Y/%m/%d/')
    monitor = models.FileField('exam monitor file', upload_to='uploads/project/%Y/%m/%d/',
                               default='uploads/default_monitor.txt')
    browser = models.FileField('exam browser file', upload_to='uploads/project/%Y/%m/%d/',
                               default='uploads/default_browser.txt')
    has_monitor = models.BooleanField('has monitor file', default=False)
    has_browser = models.BooleanField('has browser file', default=False)
    create_time = models.DateTimeField('create time', default=timezone.now())

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.create_time = timezone.now()
        return super(ExamProjects, self).save(*args, **kwargs)


class ExitMd5(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    md5 = models.CharField(max_length=128, verbose_name='md5')


class ExamMac(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    mac = models.CharField(max_length=17, verbose_name='mac')


class SolutionVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam')
    mac = models.CharField(max_length=17, verbose_name='mac')
    timestamp = models.DateTimeField(verbose_name='timestamp')
    score = models.FloatField(default=0, verbose_name='score')
    location = models.TextField(max_length=512, verbose_name='location')
