from django.db import models
from ublogging.models import Post

class Jabber(models.Model):
    post = models.ForeignKey(Post)
