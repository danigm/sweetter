from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User)
    location = models.CharField(max_length=100)
    karma = models.DecimalField(max_digits=5, decimal_places=2)
    avatar = models.ImageField(upload_to='avatars')
    votes = models.PositiveIntegerField()
    
class Group(models.Model):
    groupname = models.CharField(max_length=100,unique=True)
    date_created = models.DateField('creation date')
    
class Post(models.Model):
    userid = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text
