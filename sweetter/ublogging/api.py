from models import Option, User

'''
Api for use in sweetter plugins to provide default behavior for all
the hooks the sweetter core calls
'''

class Plugin:
    '''
    Base class for every plugin for sweetter.  It provides default
    behavior for all the hooks the sweetter core calls.  For adding
    behavior, just define the methods you want to hook in in the plugin
    class.
    '''

    def __init__(self):
        '''
        Initialize the plugin,
        This method is only called once on startup of the sweetter
        application.
        '''

        pass

    def headbar(self, context):
        '''
        Called everytime the headbar is rendered. Return a string with
        HTML that will be placed above the content. You should use Django
        templates. 
        
        Arguments:
            context -- contains: user -> the current logged in user if is
            logged in.
        '''

        return ''
    
        
    def sidebar(self, context):
        '''
        Called everytime the sidebar is rendered. Return a string with
        HTML that will be placed in the sidebar. You should use Django
        templates. 
        
        Arguments:
            context -- contains: user -> the current logged in user if is
            logged in.
        '''

        return ''
    
    def tools(self, context, post):
        '''
        Called everytime a message is rendered. Return a string with
        HTML that will be placed in the toolbar (the best option is a
        little image or button. You should use Django templates. 
        
        Arguments:
            context -- contains: user -> the current logged in user if is
            logged in.
            post -- is a Post object 
        '''            

        return ''
        
    def parse(self, value):
        '''
        Called everytime a message is rendered. Return a string with
        the text of the message.  This is useful for performing
        substitutions based on the content of the message.
        
        Arguments:
            value -- is the text of the message (unicode string)
        '''

        return value
        
    def post_list(self, value, request, user_name):
        '''
        Called everytime the index page is requested. Return a Q
        object representing a DB query.  This is useful for including
        posts in the index page.
        
        Arguments:
            value -- is the current built query (a Q object)
            request -- is the user request
            user_name -- is the user name which index will be rendered.
        '''

        return value
    
    def posting(self, request):
        '''
        Called everytime a new post is being added.
        Return True for cancelling the post.
        
        Arguments:
            request -- is the user request.
        '''

        return False
    
    def posted(self, request, post):
        '''
        Called everytime a new post has been saved.
        
        Arguments:
            request -- is the user request.
            post -- is the Post saved.
        '''

        pass

class PluginOpt:
    '''
    Define an user option to use in plugins. Each Option defined as
    attribute of a Plugin class is showed in profile page and could be
    changed and stored.
    '''
    
    def __init__(self, id, type="str", default=""):
        self.id = id
        self.type = type
        self.default = default
        self.html = ""

    def get(self, username):
        u = User.objects.get(username = username)
        opt = Option.objects.get(optid=self.id, user=u)
        return opt

    def get_filter(self, value):
        if value == True:
            value = "1"
        elif value == False:
            value = "0"

        value = str(value)
        opt = Option.objects.filter(optid=self.id, data=value)
        return opt

    def get_value(self, username):
        try:
            opt = self.get(username)
            if self.type == 'bool':
                return bool(int(opt.data))
            return opt.data
        except:
            return self.default

    def set(self, value, username):
        if self.type == 'bool':
            if value:
                value = '1'
            else:
                value = '0'

        try:
            opt = self.get(username)
            opt.data = value
        except:
            u = User.objects.get(username = username)
            opt = Option(optid=self.id, data=value, type=self.type, user=u)
        finally:
            opt.save()

    def get_html_type(self):
        if self.type in ['str', 'int']:
            type = "text"
        elif self.type == 'password':
            type = "password"
        elif self.type == 'bool':
            type = "checkbox"

        return type

    def get_html_value(self, request):
        return self.get_value(request.user.username)

