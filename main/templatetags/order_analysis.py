from django.template import Library


register = Library()


@register.filter(expects_localtime=True)
def order_analysis(order):
    if not order.payment_set.all():
        return None
    result = {
        'Доход':0,
        'Расход':0,
        'Прибыль':0,
        'Прибыль в %':0,
        'Прибыль в день':0,
        'Длительность':0,
        'Расходных операций':0}
    for payment in order.payment_set.all():
        if payment.type_operation == '+':
            result['Доход'] += int(payment.my_price)
        else:
            result['Доход'] += 0
        result['Расход'] += int(payment.my_price)
        result['Длительность'] = (order.complete_date-order.create_date).days
        result['Расходных операций'] += int(len(order.payment_set.all()))
    result['Прибыль'] = result['Доход']-result['Расход']
    if result['Доход']:
        result['Прибыль в %'] = round((result['Доход']-result['Расход'])/(result['Доход']/100),2)
    else:
        result['Прибыль в %'] = 0
    if result['Длительность']:
        result['Прибыль в день'] = round((result['Доход']-result['Расход'])/result['Длительность'], 2)
    else:
        result['Прибыль в день'] = result['Прибыль']
    return result.items()


