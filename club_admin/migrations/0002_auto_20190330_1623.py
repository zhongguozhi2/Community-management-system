# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-30 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club_admin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubadmin',
            old_name='name',
            new_name='username',
        ),
    ]