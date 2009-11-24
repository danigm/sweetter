from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import string
import random

def generate_apikey():
    chars = string.letters + string.digits
    return "".join([random.choice(chars) for i in range(20)])

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    apikey = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.apikey = generate_apikey()
        super(Profile, self).save(*args, **kwargs)

class Option(models.Model):
    optid = models.CharField(max_length=20)
    data = models.TextField()
    #type could be:
    #   int, str, password, bool
    type = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    unique_together = ("optid", "user")

    def __unicode__(self):
        return '<%s, %s, %s>' % (self.user.username, self.optid, self.data)
        
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
from django.forms import ModelForm, ValidationError

# RegisterProfile
class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError(u'Email addresses must be unique.')
        return email

