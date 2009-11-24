
class Flash_msg:
    def __init__(self, msg, type):
        self.msg = msg
        self.type = type

    def is_error(self):
        return self.type == "error"

    def is_info(self):
        return not self.is_error()

def set_flash(request, msg, type="info"):
    ''' type could be info or error '''
    request.session['flash'] = Flash_msg(msg, type)
    
def get_flash(request):
    f = request.session.get('flash', '')
    request.session['flash'] = ''
    return f

def context_processor(request):
    flash = get_flash(request)
    return {'flash': flash}
