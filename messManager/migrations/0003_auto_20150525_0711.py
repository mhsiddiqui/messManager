# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messManager', '0002_webuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webuser',
            name='staff',
        ),
        migrations.RemoveField(
            model_name='webuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='WebUser',
        ),
    ]
