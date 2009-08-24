from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    location = models.CharField(max_length=100)
    karma = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    avatar = models.ImageField(upload_to='avatars')
    votes = models.PositiveIntegerField(default=0)
    
class Group(models.Model):
    groupname = models.CharField(max_length=100,unique=True)
    date_created = models.DateField('creation date')
    
class Post(models.Model):
    userid = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text

# SIGNALS AND LISTENERS
from django.contrib.auth.models import User


# User
def user_post_save(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    profile, new = Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)