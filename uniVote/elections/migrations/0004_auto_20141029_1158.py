# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0003_voter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voter',
            old_name='is_approved',
            new_name='approved',
        ),
    ]
