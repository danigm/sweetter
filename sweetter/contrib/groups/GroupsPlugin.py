
from django.template.loader import render_to_string


class Group:
    def __init__(self):
        pass
        
    def sidebar(self, context):
        return render_to_string('groupsidebar.html', {
                
            }, context_instance=context)
    
    def tools(self, context, post):
        return ''
