#!/usr/bin/python
# -*- coding: utf-8 -*-

from ublogging.register import adduser
from ublogging.uapi import new_post, Request_moc

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

for i in users:
    u = adduser(*i)
    for p in posts:
        new_post(u, p, Request_moc(u))
