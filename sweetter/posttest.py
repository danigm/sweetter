#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from ublogging.models import User
from ublogging.uapi import new_post, Request_moc

posts = (
    "probando sweetter 3.0",
    "escribo un post con referencia @pepe",
    "un post con enlaces http://sweetter.net, http://danigm.net",
    "un post con varios replies @pepe, @juan, @nota",
    "un post con tíldes y ñ",
    "arrrrrrrrrrrrrrrrrrrrrrrg",
    )

u = User.objects.get(username = 'culebra')
p = random.choice(posts)
new_post(u, p, Request_moc(u))
