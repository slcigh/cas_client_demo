from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50, default=u'abc')

