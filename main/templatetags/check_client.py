from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def check_client(order):
    return order.client_set.all()
