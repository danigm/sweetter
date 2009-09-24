class Plugin:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        return ''
                
    def tools(self, context, post):
        return ''
        
    def parse(self, value):
        return value
        
    def post_list(self, value, request, user_name):
        return value
    
    def posting(self, request):
        return False
    
    def posted(self, request, post):
        pass
