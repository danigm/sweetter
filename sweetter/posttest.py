#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from sweetter.ublogging.views import new_post
from sweetter.ublogging.models import User

posts = (
    "probando sweetter 3.0",
    "escribo un post con referencia @pepe",
    "un post con enlaces http://sweetter.net, http://danigm.net",
    "un post con varios replies @pepe, @juan, @nota",
    "un post con tíldes y ñ",
    "arrrrrrrrrrrrrrrrrrrrrrrg",
    )

class request_moc:
    def __init__(self, user):
        self.user = user

u = User.objects.get(username = 'culebra')
p = random.choice(posts)
new_post(u, p, request_moc(u))

