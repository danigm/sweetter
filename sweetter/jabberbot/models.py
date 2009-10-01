from django.db import models
from django.contrib.auth.models import User

class Jabber(models.Model):
    user = models.ForeignKey(User)
    jid = models.CharField(max_length=140)
    active = models.BooleanField()
    enabled = models.BooleanField()

    def __unicode__(self):
        return self.jid
