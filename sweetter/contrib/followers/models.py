from django.db import models
from django.contrib.auth.models import User
from sweetter.ublogging.models import *

class Follower (models.Model):    
    user = models.ForeignKey(User, related_name='users')
    follower = models.ForeignKey(User, related_name='followers')