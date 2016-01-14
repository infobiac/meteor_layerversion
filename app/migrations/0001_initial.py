# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('prof_pic', models.CharField(max_length=300)),
                ('first_log_in', models.BooleanField(default=True)),
                ('email', models.CharField(max_length=100)),
                ('idnumber', models.CharField(max_length=100, serialize=False, primary_key=True)),
            ],
        ),
    ]
