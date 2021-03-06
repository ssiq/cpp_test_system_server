# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-13 10:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_question_create_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['-begin_time']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-create_time']},
        ),
        migrations.AlterField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 13, 10, 54, 6, 287690, tzinfo=utc), verbose_name='create time'),
        ),
    ]
