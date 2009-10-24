from django.db import models
from django.contrib.auth.models import User

class Jabber(models.Model):
    active = models.BooleanField()
