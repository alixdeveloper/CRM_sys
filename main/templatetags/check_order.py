from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def check_order(order):
    return order.product_set.all()
