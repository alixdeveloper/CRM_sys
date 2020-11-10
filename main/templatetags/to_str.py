from django.template import Library
import datetime
from main.models import Client
register = Library()


@register.filter(expects_localtime=True)
def to_str(data):
    return str(data)

