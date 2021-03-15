from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def to_str(data):
    return str(data)

