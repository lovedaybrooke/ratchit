# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polladmin', '__first__'),
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='poll',
            field=models.ForeignKey(related_name='ratings', default=1, to='polladmin.Poll'),
            preserve_default=False,
        ),
    ]
