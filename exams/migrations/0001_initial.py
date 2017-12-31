# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-12-31 12:23
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name="exam's name")),
                ('begin_time', models.DateTimeField(verbose_name="exam's begin time")),
                ('end_time', models.DateTimeField(verbose_name="exam's end time")),
                ('isHomework', models.BooleanField(default=False, verbose_name='is homework?')),
                ('isPrivate', models.BooleanField(default=False, verbose_name='is private?')),
            ],
            options={
                'ordering': ['-begin_time'],
                'verbose_name': '\u8003\u8bd5',
                'verbose_name_plural': '\u8003\u8bd5',
            },
        ),
        migrations.CreateModel(
            name='ExamMac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=17, verbose_name='mac')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='ExamProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.FileField(upload_to='uploads/log/%Y/%m/%d/', verbose_name='exam log')),
                ('project', models.FileField(upload_to='uploads/project/%Y/%m/%d/', verbose_name='exam project')),
                ('monitor', models.FileField(default='uploads/default_monitor.txt', upload_to='uploads/project/%Y/%m/%d/', verbose_name='exam monitor file')),
                ('browser', models.FileField(default='uploads/default_browser.txt', upload_to='uploads/project/%Y/%m/%d/', verbose_name='exam browser file')),
                ('has_monitor', models.BooleanField(default=False, verbose_name='has monitor file')),
                ('has_browser', models.BooleanField(default=False, verbose_name='has browser file')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2017, 12, 31, 12, 23, 6, 967709, tzinfo=utc), verbose_name='create time')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='ExamQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(verbose_name='question weights in this exam')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamRandomMd5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=128, verbose_name='md5')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='ExitMd5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md5', models.CharField(max_length=128, verbose_name='md5')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='question name')),
                ('description', models.TextField(verbose_name='question description')),
                ('content', models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='question content')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2017, 12, 31, 12, 23, 6, 964651, tzinfo=utc), verbose_name='create time')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u9898\u76ee',
                'verbose_name_plural': '\u9898\u76ee',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(verbose_name='score')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Question', verbose_name='question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=17, verbose_name='mac')),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2017, 12, 31, 12, 23, 6, 969946, tzinfo=utc), verbose_name='timestamp')),
                ('log', models.FileField(upload_to='uploads/log_new/%Y/%m/%d/', verbose_name='exam log zip')),
                ('solution', models.FileField(upload_to='uploads/solution/%Y/%m/%d/', verbose_name='exam solution zip')),
                ('score', models.FileField(upload_to='uploads/score/%Y/%m/%d/', verbose_name='exam log zip')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='examquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Question', verbose_name='question'),
        ),
    ]
