from django.db import models
from sweetter.ublogging.models import User
from sweetter.ublogging.models import generate_apikey

class Recover(models.Model):
    user = models.ForeignKey(User, unique=True)
    key = models.CharField(max_length=20)

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.key = generate_apikey()
        super(Recover, self).save(*args, **kwargs)

