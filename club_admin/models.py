from django.db import models


class ClubAdmin(models.Model):
    username = models.CharField(max_length=32, unique=True, blank=False, null=False)
    password = models.CharField(max_length=256)
    token = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = 'club_admin'
