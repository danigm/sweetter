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

