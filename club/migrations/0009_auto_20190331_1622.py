# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-31 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_auto_20190330_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$36000$S24XBiXXSfRh$ZOgfx/FNYqicUxJiYvvMY0ovMxpHHe5oY1C1A6dNDCI=', max_length=256),
        ),
    ]
