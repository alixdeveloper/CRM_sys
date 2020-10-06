from django.template import Library
import datetime

register = Library()


@register.filter(expects_localtime=True)
def parse_iso(value):
    return value.strftime('%Y-%m-%d')\


