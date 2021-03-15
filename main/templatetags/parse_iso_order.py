from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def parse_iso_order(value):
    return value.strftime('%H:%M %d.%m.%y')
