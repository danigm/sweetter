from decimal import Decimal
from sweetter.contrib.karma.models import Karma
from django.template.loader import render_to_string

class KarmaCount:      
    def __init__(self):
        pass
        
    def sidebar(self, context):
        if context['user'] and not context['user'].is_authenticated():
            return ''
        else:
            try:
                k = Karma.objects.get(user=context['user'])
                k.value = k.value + 0.01
                k.save()
            except:
                k=Karma(user=context['user'],value=0)
                k.save()
            return render_to_string('karmasidebar.html', { 'karma': k }, context_instance=context)
                
    def tools(self, context, post):
        return ''
        
    def parse(self, value):
        return value