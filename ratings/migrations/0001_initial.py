# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ratings.models


class Migration(migrations.Migration):

    dependencies = [
        ('polladmin', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_hash', models.CharField(default=ratings.models._createHash, unique=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('category', models.ForeignKey(related_name='ratings', to='polladmin.Category')),
                ('option', models.ForeignKey(related_name='ratings', to='polladmin.Option')),
                ('rater', models.ForeignKey(related_name='ratings', to='ratings.Rater')),
            ],
        ),
    ]
