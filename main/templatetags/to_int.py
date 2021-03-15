from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def to_int(payment):
    return payment.client_count-payment.my_count

