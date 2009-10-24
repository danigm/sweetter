from sweetter.ublogging import api

class JabberPlugin(api.Plugin):
    __plugin_name__ = 'jabberbot'

    juser = api.PluginOpt('jabber_user')
    enabled = api.PluginOpt('jabberbot_enabled',
                            type="bool",
                            default=False)
