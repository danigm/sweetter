#!/usr/bin/python

#export PYTHONPATH=/home/danigm/sweetter3/ export DJANGO_SETTINGS_MODULE=settings

from hashlib import md5

import sys
import os
os.environ['PYTHONPATH'] = "/home/danigm/sweetter3"
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
import random
import string
sys.path += [os.path.abspath(".."), os.path.abspath("../..")]

import s2model
from ublogging.models import *
from contrib.followers.models import Follower

def generate():
    return "".join([random.choice(string.letters+string.digits) for _ in range(11)])

def main():
    users_dict = {}

    users = s2model.User.select()
    for u in users:
        x = User(username=u.user_name, email=u.email_address,
                password_md5=u.password)
        x.save()
        users_dict[u.user_name] = x

        sweets = s2model.Sweets.select(s2model.Sweets.q.userID == u.id)
        for s in sweets:
            post = Post(text=s.comment, user=x, pub_date=s.created)
            post.save()

    for u in users:
        x = users_dict[u.user_name]
        followings = s2model.Followers.select(s2model.Followers.q.followerID == u.id)
        for f in followings:
            f1 = Follower(user=users_dict[f.following.user_name], follower=x)
            f1.save()

