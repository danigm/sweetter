from django.conf import settings
from django.db import models

from ublogging.models import Profile


class Group(models.Model):
    name = models.CharField(max_length=100,unique=True)
    date_created = models.DateTimeField('creation date', auto_now=True)
    icon = models.ImageField(upload_to='groups')
    users = models.ManyToManyField(Profile)
