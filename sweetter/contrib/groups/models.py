from django.db import models
from django.contrib.auth.models import User
from sweetter.ublogging.models import *
    
class Group(models.Model):
    name = models.CharField(max_length=100,unique=True)
    date_created = models.DateField('creation date')