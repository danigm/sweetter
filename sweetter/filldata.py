#!/usr/bin/python
# -*- coding: utf-8 -*-

from sweetter.ublogging.register import adduser
from sweetter.ublogging.views import new_post

users = (
    ('pepe', '123', 'pepe@pepe.com'),
    ('juan', '123', 'juan@pepe.com'),
    ('jose', '123', 'jose@pepe.com'),
    ('nota', '123', 'nota@pepe.com'),
    ('cabeza', '123', 'cabeza@pepe.com'),
    ('culebra', '123', 'culebra@pepe.com'),
    )

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

for i in users:
    u = adduser(*i)
    for p in posts:
        new_post(u, p, request_moc(u))

