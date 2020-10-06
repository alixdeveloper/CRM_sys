from django.template import Library

register = Library()


@register.filter(expects_localtime=True)
def login_check(request):
    if request.session.get('login', False):
        return True
    else:
        return False


