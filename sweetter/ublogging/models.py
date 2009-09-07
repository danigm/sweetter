from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)    
    
    def __unicode__(self):
        return self.user.username
        
class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __unicode__(self):
        return self.text

# SIGNALS AND LISTENERS
from django.contrib.auth.models import User


# User
def user_post_save(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    profile, new = Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)

# FORMS
from django.forms import ModelForm

# RegisterProfile
class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']