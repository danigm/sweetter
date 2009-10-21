#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.append("../..")
sys.path.append("..")

from jabberbot.jabberbot import JabberBot
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
        print "jabberbot on"
        #return sweet_utils.jabber_on(user)

    def bot_off(self, mess, args):
        'Desactiva el bot. Uso:\n\toff\n'
        f = mess.getFrom()
        user = f.getNode()+'@'+f.getDomain()
        print "jabberbot on"
        #return sweet_utils.jabber_off(user)

    def bot_post(self, mess, args):
        'Envia un comentario a sweetter. Uso:\n\tpost <comentario>\n'
        f = mess.getFrom()
        user = f.getNode()+'@'+f.getDomain()
        print "jabberpost", user, args
        #return sweet_utils.jabber_post(user, args)

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

    def send_all(self, lista, comentario):
        for i in lista:
            self.send(i, comentario)

    def idle_proc(self):
        lista = []
        print "idle proc"
        #lista = sweet_utils.jabber_authorize()
        for u in lista:
            self.conn.Roster.Authorize(u)

def main():
    bot = SystemInfoJabberBot(settings.JB_USER, settings.JB_PASSWD)
    bot.serve_forever()

if __name__ == '__main__':
    main()
