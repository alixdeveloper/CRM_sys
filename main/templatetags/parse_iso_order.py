from django.template import Library
import datetime

register = Library()


@register.filter(expects_localtime=True)
def parse_iso_order(value):
    return value.strftime('%H:%M %d.%m.%y')
