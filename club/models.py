from django.db import models

from club.con_common import MEMBER_DEFAULT_PASSWORD


class Club(models.Model):
    name = models.CharField(max_length=32, unique=True, blank=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'club'


class Member(models.Model):
    sid = models.CharField(unique=True, blank=False, null=False, max_length=12)
    name = models.CharField(max_length=16, null=True)
    password = models.CharField(blank=False, null=False, max_length=256, default=MEMBER_DEFAULT_PASSWORD)
    phone = models.CharField(max_length=11, null=True)
    qq = models.CharField(max_length=11, null=True)
    icon = models.CharField(max_length=256, null=True)
    token = models.CharField(max_length=256, null=True)
    is_delete = models.BooleanField(default=False)
    club = models.ManyToManyField(Club, related_name='member_club')
    admin = models.ManyToManyField(Club, related_name='member_admin')

    class Meta:
        db_table = 'member'
