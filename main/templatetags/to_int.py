from django.template import Library
import datetime
from main.models import Client
register = Library()


@register.filter(expects_localtime=True)
def to_int(payment):
    return float(payment.client_price)-float(payment.my_price)

