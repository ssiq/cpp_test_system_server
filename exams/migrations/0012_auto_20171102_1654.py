# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-11-02 08:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_auto_20171102_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examprojects',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 2, 8, 54, 8, 47143, tzinfo=utc), verbose_name='create time'),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 2, 8, 54, 8, 43939, tzinfo=utc), verbose_name='create time'),
        ),
    ]