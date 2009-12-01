#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
sys.path.append(".")

import os

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from jabberbot.jabberbot import JabberBot
from jabberplugin import JabberPlugin as plugin
from sweetter.jabberbot.models import Jabber
from sweetter.ublogging.uapi import new_post, Request_moc
import settings
import datetime

class SystemInfoJabberBot(JabberBot):
    '''
    Soy terron, el bot de sweetter.
    Lo primero que tienes que hacer es validar que esta
    es tu cuenta con el comando validate seguido de tu apikey

    validate cxa123asdasdfasq2

    Luego cada cosa que escribas se posteará en sweetter y
    yo te diré quién ha escrito en sweeter.

    Gracias por jugar :P

    Aquí una lista de comandos soportados (usa help <comando>
    para mostrar la ayuda de un comando concreto):

    '''

    def unknown_command( self, mess, cmd, args):
        return self.bot_post(mess=mess, args = cmd+' '+args)

    def bot_on(self, mess, args):
        'Activa el bot. Uso:\n\ton\n'
        f = mess.getFrom()
        user = f.getNode()+'@'+f.getDomain()
        try:
            suser = plugin.juser.get_filter(user)[0]
            plugin.actived.set(True, suser.user.username)
            return "jabberbot activado"
        except:
            return "fallo :("

    def bot_off(self, mess, args):
        'Desactiva el bot. Uso:\n\toff\n'
        f = mess.getFrom()
        user = f.getNode()+'@'+f.getDomain()
        try:
            suser = plugin.juser.get_filter(user)[0]
            plugin.actived.set(False, suser.user.username)
            return "jabberbot desactivado"
        except:
            return "fallo :("

    def bot_post(self, mess, args):
        'Envia un comentario a sweetter. Uso:\n\tpost <comentario>\n'
        f = mess.getFrom()
        user = f.getNode()+'@'+f.getDomain()
        try:
            suser = plugin.juser.get_filter(user)[0]
            request = Request_moc(suser.user)
            new_post(suser.user, args, request)
        except:
            return "fallo :("

    def bot_(self, mess, args):
        ' '
        pass

    #def bot_validate(self, mess, args):
    #    'Valida una cuenta. Uso:\n\tvalidate <apikey>\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_validate(user, args)

    #def bot_validation(self, mess, args):
    #    'Devuelve el estado de validación de una cuenta. Uso:\n\tvalidation\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_validation(user)

    #def bot_statistics(self, mess, args):
    #    'Devuelve algunas estadísticas. Uso:\n\tstatistics\n'
    #    return sweet_utils.jabber_statistics()

    #def bot_show_profile(self, mess, args):
    #    'Devuelve información del perfil de un usuario. Uso:\n\tshow_profile [<usuario>]\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_show_profile(user, args)

    #def bot_search_users(self, mess, args):
    #    'Busca usuarios. Si no se especifica usuario se buscan todos. Uso:\n\tsearch_users [<cadena> [page <number>]]\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_search_users(user, args)

    #def bot_followers(self, mess, args):
    #    'Lista los followers. Si no se especifica usuario se mostrarán tus followers. Uso:\n\tfollowers [<usuario>] [page <number>]\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_follow_something(user, args, "followers")

    #def bot_followings(self, mess, args):
    #    'Lista los followings. Si no se especifica usuario se mostrarán tus followings. Uso:\n\tfollowings [<usuario>] [page <number>]\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_follow_something(user, args, "followings")

    #def bot_vote(self, mess, args):
    #    'Vota un sweet. Uso:\n\tvote (sweet <sweetid> | last <usuario>) (+1 | -1)\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_vote(user, args)

    #def bot_edit(self, mess, args):
    #    'Edita un sweet. Uso:\n\tedit (sweet <sweetid> | last) <texto del sweet>\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_edit(user, args)

    #def bot_delete(self, mess, args):
    #    'Elimina un sweet. Uso:\n\tdelete (sweet <sweetid> | last)\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_delete(user, args)

    #def bot_follow(self, mess, args):
    #    'Followea/desfollowea/mira el estado de follower de un usuario. Uso:\n\tfollow [status | not] user <usuario>\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_follow(user, args)

    #def bot_location(self, mess, args):
    #    'Muestra/Actualiza el location del usuario. Uso:\n\tlocation [<location>]\n'
    #    f = mess.getFrom()
    #    user = f.getNode()+'@'+f.getDomain()
    #    return sweet_utils.jabber_location(user, args)

    def send_all(self):
        comments = Jabber.objects.all()
        all = plugin.enabled.get_filter(True)
        
        for comment in comments:
            for i in all:
                if plugin.actived.get_value(i.user.username):
                    jid = plugin.juser.get_value(i.user.username)
                    sayed = comment.post.user.username
                    sayed += ": " + comment.post.text
                    self.send(jid, sayed)
            comment.delete()

    def idle_proc(self):
        lista = []
        all = plugin.enabled.get_filter(True)
        for u in all:
            jid = plugin.juser.get_value(u.user.username)
            self.conn.Roster.Authorize(jid)

        self.send_all()

def main():
    bot = SystemInfoJabberBot(settings.JB_USER, settings.JB_PASSWD)
    bot.serve_forever()

if __name__ == '__main__':
    main()
