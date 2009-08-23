from django.db import models

class Post(models.Model):
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
	    return self.text
