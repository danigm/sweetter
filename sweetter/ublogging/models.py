import string
import random

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm, ValidationError

def generate_apikey():
    chars = string.letters + string.digits
    return "".join([random.choice(chars) for i in range(20)])

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    apikey = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.apikey = generate_apikey()
            self.location = "sweetter city"
            self.url = reverse("ublogging.views.user", kwargs={'user_name':self.user.username})
        super(Profile, self).save(*args, **kwargs)

    def regen_apikey(self):
        self.apikey = generate_apikey()

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
    #pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.text

def user_post_save(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    profile, new = Profile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)

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
