# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-30 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0006_auto_20190330_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$36000$iOF3KAJI03kH$aU+5Segd/cHcJvEVZ6qEhuoJaLaY2rfHG/3iZ5oS4eg=', max_length=256),
        ),
    ]
