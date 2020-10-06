from django.template import Library
import datetime

register = Library()


@register.filter(expects_localtime=True)
def get_orders_of_product(product):
    return product.orders.all()
