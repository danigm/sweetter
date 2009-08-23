from django.db import models

class User(models.Model):	
	username = models.CharField(max_length=100,unique=True)
	password = models.CharField(max_length=200)
	date_join = models.DateField('join date')
	location = models.CharField(max_length=100)
	karma = models.DecimalField(max_digits=5, decimal_places=2)
	email = models.EmailField(max_length=75)
	avatar = models.ImageField('avatars')
	votes = models.PositiveIntegerField()
	
class Group(models.Model):
	groupname = models.CharField(max_length=100,unique=True)
	date_created = models.DateField('creation date')
	
class Role(models.Model):
	name = models.CharField(max_length=100);	

class Membership(models.Model):
	userid = models.ForeignKey(User)
	groupid = models.ForeignKey(Group)
	roleid = models.ForeignKey(Role)

class Post(models.Model):
	userid = models.ForeignKey(User)
    text = models.CharField(max_length=140)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
	    return self.text
