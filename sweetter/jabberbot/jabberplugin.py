from ublogging import api
from jabberbot.models import Jabber


class JabberPlugin(api.Plugin):
    __plugin_name__ = 'jabberbot'

    juser = api.PluginOpt('jabber_user')
    enabled = api.PluginOpt('jabberbot_enabled',
                            type="bool",
                            default=False)
    actived = api.PluginOpt('jabberbot_actived',
                            type="bool",
                            default=True)

    def posted(self, request, post):
        j = Jabber(post=post)
        j.save()
