from django.db import models
from sweetter.ublogging.models import Post

class Jabber(models.Model):
    post = models.ForeignKey(Post)
