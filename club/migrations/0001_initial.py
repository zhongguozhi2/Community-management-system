# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-25 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'club',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=16)),
                ('password', models.CharField(default='000000', max_length=16)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('qq', models.CharField(max_length=11, null=True, unique=True)),
                ('icon', models.CharField(max_length=256, null=True)),
                ('token', models.CharField(max_length=256, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('admin', models.ManyToManyField(related_name='member_admin', to='club.Club')),
                ('club', models.ManyToManyField(related_name='member_club', to='club.Club')),
            ],
            options={
                'db_table': 'member',
            },
        ),
    ]
