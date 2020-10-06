from django.template import Library
import datetime
from main.models import Client
register = Library()


@register.filter(expects_localtime=True)
def get_clients_of_order(order):
    return order.client_set.all()

