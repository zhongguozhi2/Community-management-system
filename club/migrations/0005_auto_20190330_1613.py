# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-30 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0004_auto_20190329_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$36000$Wgpkylk9kMVY$CHXpU90I8gC2CoUvPPPYxPXLUPoFgULZ30kfLgJ+Ick=', max_length=256),
        ),
    ]