from django.db import models
from sweetter.ublogging.models import Profile
    
class Group(models.Model):
    name = models.CharField(max_length=100,unique=True)
    date_created = models.DateField('creation date')
    users = models.ManyToManyField(Profile)