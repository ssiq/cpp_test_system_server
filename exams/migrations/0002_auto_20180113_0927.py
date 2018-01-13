# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-13 01:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('log', models.FileField(upload_to='uploads/log_new/%Y/%m/%d/', verbose_name='exam log zip')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='NewScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('score', models.FileField(upload_to='uploads/score/%Y/%m/%d/', verbose_name='exam score zip')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='', max_length=200, verbose_name='version')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('solution', models.FileField(upload_to='uploads/solution/%Y/%m/%d/', verbose_name='exam solution zip')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam', verbose_name='exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AlterField(
            model_name='examprojects',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='create time'),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='create time'),
        ),
    ]