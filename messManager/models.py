import datetime
from django.contrib.auth.models import User, Group

from django.db import models
from django.utils import timesince

class Mess(models.Model):
    mess_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    mess_admin = models.ForeignKey(User)


class MemberMess(models.Model):
    mess = models.ForeignKey(Mess)
    user = models.ForeignKey(User)