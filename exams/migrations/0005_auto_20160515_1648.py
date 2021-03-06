# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-15 08:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_auto_20160513_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['-begin_time'], 'verbose_name': '\u8003\u8bd5', 'verbose_name_plural': '\u8003\u8bd5'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-create_time'], 'verbose_name': '\u9898\u76ee', 'verbose_name_plural': '\u9898\u76ee'},
        ),
        migrations.AddField(
            model_name='exam',
            name='isHomework',
            field=models.BooleanField(default=False, verbose_name='is homework?'),
        ),
        migrations.AlterField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 15, 8, 48, 49, 112127, tzinfo=utc), verbose_name='create time'),
        ),
    ]
