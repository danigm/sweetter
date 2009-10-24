from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)    
    
    def __unicode__(self):
        return self.user.username

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
from django.forms import ModelForm

# RegisterProfile
class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    class Meta:
        model = User
        fields = ('username', 'email')
