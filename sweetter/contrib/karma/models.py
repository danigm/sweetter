from django.db import models
from django.contrib.auth.models import User
from sweetter.ublogging.models import *

class Karma (models.Model):    
    user = models.ForeignKey(User, unique=True)
    value = models.FloatField()