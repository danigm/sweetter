'''
Base class for every plugin for sweetter.
It provides default behavior for all the hooks the sweetter core calls.
For adding behavior, just define the methods you want to hook in
in the plugin class.
'''
class Plugin:
    '''
    Initialize the plugin,
    This method is only called once on startup of the sweetter application.
    '''
    def __init__(self):
        pass
        
    '''
    Called everytime the sidebar is rendered. Return a string with HTML that will be
    placed in the sidebar. You should use Django templates. 
    
    context contains: user -> the current logged in user if is logged in.
    '''
    def sidebar(self, context):
        return ''
    
    '''
    Called everytime a message is rendered. Return a string with HTML that will be
    placed in the toolbar (the best option is a little image or button. You should use 
    Django templates. 
    
    context contains: user -> the current logged in user if is logged in.
    post is a Post object 
    '''            
    def tools(self, context, post):
        return ''
        
    '''
    Called everytime a message is rendered. Return a string with the text of the message.
    This is useful for performing substitutions based on the content of the message.
    
    value is the text of the message (unicode string)
    '''
    def parse(self, value):
        return value
        
    '''
    Called everytime the index page is requested. Return a Q object representing a DB query.
    This is useful for including posts in the index page.
    
    value is the current built query (a Q object)
    request is the user request
    user_name is the user name which index will be rendered.
    '''
    def post_list(self, value, request, user_name):
        return value
    
    '''
    Called everytime a new post is being added.
    Return True for cancelling the post.
    
    request is the user request.
    '''
    def posting(self, request):
        return False
    
    '''
    Called everytime a new post has been saved.
    
    request is the user request.
    post is the Post saved.
    '''
    def posted(self, request, post):
        pass
