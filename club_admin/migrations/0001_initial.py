# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-30 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClubAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('token', models.CharField(default=None, max_length=256)),
            ],
            options={
                'db_table': 'club_admin',
            },
        ),
    ]