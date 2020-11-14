from django.db import models
from decimal import Decimal
from django.utils import timezone


class Order(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField('дата приема заказа')
    complete_date = models.DateTimeField('дата завершения заказа', default=timezone.now)
    weight = models.DecimalField(max_digits=65, decimal_places=2)
    preorder_weight = models.DecimalField(max_digits=65, decimal_places=2, default=Decimal(0))
    price = models.DecimalField(max_digits=65, decimal_places=2)
    prepayment = models.DecimalField(max_digits=65, decimal_places=2,default=Decimal(0))
    status = models.CharField(max_length=255, default='Создан')
    ads = models.CharField(max_length=255)

    def __str__(self):
        return f'Заказ {self.id} от {self.create_date}'

    def sum_weight_product(self):
        products = self.product_set.all()
        result = float(0)
        if products:
            for product in products:
                result += product.weight
        return result



    def payments_result(self):
        payments = self.payment_set.all()
        order_table = list()
        order_report = {
            'Стоимость для клиента': Decimal(0.00),
            'Доход':Decimal(0.00),
            'Остаток':Decimal(0.00),
            'Моя работа':Decimal(0.00),
                        'Наценка':Decimal(0.00),
                        'Затраты':Decimal(0.00),
                        'Прибыль':Decimal(0.00),
                        'Прибыль в %':0,
                        'Прибыль в день':Decimal(0.00),
                        'Длительность':0,
                        'Затратыных операций':0}
        order_report['Длительность'] = (self.complete_date - self.create_date).days
        for payment in payments:
            order_table.append([payment.name,
                                round(Decimal(payment.my_count),2),
                                round(Decimal(payment.client_count-payment.my_count)),
                                round(Decimal(payment.client_count))])
            if payment.type_operation != '+':
                order_report['Наценка'] += payment.client_count-payment.my_count
            if payment.type_operation == '=':
                order_report['Моя работа'] += payment.my_count
            if payment.type_operation == '+':
                order_report['Доход'] += payment.my_count
            else:
                order_report['Затратыных операций'] += 1
                order_report['Затраты'] += payment.my_count
                order_report['Стоимость для клиента'] += payment.client_count
        if order_report['Доход'] == 0:
            order_report['Прибыль в %'] = round(order_report['Доход'],2)
        else:
            order_report['Прибыль в %'] = round((order_report['Доход']-order_report['Затраты']+order_report['Моя работа'])/(order_report['Доход']/100),2)
        if order_report['Длительность'] == 0:
            order_report['Прибыль в день'] = round(order_report['Доход']-order_report['Затраты'],2)

        else:
            order_report['Прибыль в день'] = round((order_report['Доход']-order_report['Затраты']+order_report['Моя работа'])/order_report['Длительность'],2)
        order_report['Прибыль'] = order_report['Доход'] - order_report['Затраты']
        order_report['Доход'] = round(order_report['Доход'],2)
        order_report['Затраты'] = round(order_report['Затраты'],2)
        order_report['Прибыль'] = Decimal(round(order_report['Прибыль'],2))
        order_report['Наценка'] = round(order_report['Наценка'],2)
        order_report['Остаток'] = round(order_report['Стоимость для клиента']-order_report['Доход'],2)
        order_report['Моя работа'] = Decimal(round(order_report['Моя работа'],2))

        for k,v in order_report.items():
            if k in ['Доход','Затраты','Прибыль','Прибыль в день', 'Стоимость для клиента','Моя работа','Наценка','Остаток']:
                order_report[k] =str(order_report[k])+' ₽'
            if k in ['Прибыль в %']:
                order_report[k] = str(order_report[k]) + ' %'
            if k in ['Длительность']:
                order_report[k] = str(order_report[k]) + ' дней'
        return {'order_table': order_table, 'order_report': order_report}


class Client(models.Model):
    """Many-to-many relationships"""
    first_name = models.CharField('имя', max_length=255)
    last_name = models.CharField('фамилия', max_length=255)
    middle_name = models.CharField(verbose_name='отчество', max_length=255)
    phone = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    orders = models.ManyToManyField(Order)
    communication_type = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'


class Product(models.Model):
    """Many-to-one relationships"""
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField('дата завершения заказа', default=timezone.now)
    complete_date = models.DateTimeField('дата завершения заказа', default=timezone.now)
    preorder_weight = models.DecimalField(max_digits=65, decimal_places=2, default=Decimal(0))
    category = models.CharField(max_length=255, default='')
    material = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    status = models.CharField(max_length=255, default='Создан')
    size = models.FloatField(default=0)
    photo = models.CharField(max_length=255)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f'Изделие "{self.name}" связано с {len(self.orders.all())} заказами'


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)


class Comment(models.Model):
    message = models.CharField(max_length=255, default="")
    date = models.DateTimeField()
    orders = models.ManyToManyField(Order)
    comment_type = models.CharField(max_length=255,default='comment')
    prev = models.CharField(max_length=255, default="")
    new = models.CharField(max_length=255, default="")
    place = models.CharField(max_length=255, default="")
    identification = models.CharField(max_length=255, default="")

class Payment(models.Model):
    name = models.CharField(max_length=255)
    my_count = models.DecimalField(max_digits=65, decimal_places=2)
    client_count = models.DecimalField(max_digits=65, decimal_places=2)
    type_operation = models.CharField(max_length=25)
    orders = models.ManyToManyField(Order)





