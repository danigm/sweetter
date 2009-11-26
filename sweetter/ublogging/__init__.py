import settings
import sys

plugins = []
for p in settings.INSTALLED_PLUGINS:
    modname, clazzname = p.rsplit('.', 1)    
    mod = __import__(modname)
    mod = sys.modules[modname]
    classobj = getattr(mod, clazzname)
    plugins.append(classobj())

