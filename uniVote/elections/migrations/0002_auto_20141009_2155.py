# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('candidate_name', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('election_text', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name=b'date election starts')),
                ('end_date', models.DateTimeField(verbose_name=b'date election ends')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(to='elections.Election'),
            preserve_default=True,
        ),
    ]
