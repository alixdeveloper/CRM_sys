from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.db.models import Q


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

    def get_first_client(self):
        client = self.client_set.first()
        return client

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
            'Предоплата':Decimal(0.00),
            'Остаток':Decimal(0.00),
            'Доход':Decimal(0.00),
            'Расход':Decimal(0.00),
            'Прибыль':Decimal(0.00),
            'Наценка':Decimal(0.00),
            'Прибыль в %':0,
        }
        for payment in payments:
            if payment.type_operation == 'predoplata':
                order_report['Предоплата'] += payment.my_count
                order_report['Доход'] += payment.my_count
            elif payment.type_operation == 'rabota':
                order_report['Доход'] += payment.my_count

            elif payment.type_operation == 'dohod':
                order_report['Стоимость для клиента'] += payment.my_count
            elif payment.type_operation == 'rashod':
                order_report['Стоимость для клиента'] += payment.client_count
                order_report['Доход'] += payment.client_count-payment.my_count
                order_report['Расход'] += payment.my_count
                order_report['Наценка'] += payment.client_count-payment.my_count
        order_report['Остаток'] += order_report['Стоимость для клиента'] - order_report['Предоплата']
        order_report['Прибыль'] += order_report['Доход'] - order_report['Расход']
        if order_report['Расход']:
            order_report['Прибыль в %'] += round(((order_report['Прибыль'] * 100) / order_report['Расход']),2)
        else:
            order_report['Прибыль в %'] = 0
        for k,v in order_report.items():
            if k in ['Стоимость для клиента','Предоплата','Остаток','Доход', 'Расход','Прибыль','Наценка', 'Прибыль в день']:
                order_report[k] =str(order_report[k])+'\xa0₽'
            if k in ['Прибыль в %']:
                order_report[k] = str(order_report[k]) + '\xa0%'
        return order_report


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

    def get_label(self):
        return self.first_name or self.last_name or self.middle_name



class ProductCategory(models.Model):
    name = models.CharField(max_length=255)


class Comment(models.Model):
    message = models.CharField(max_length=255, default="")
    date = models.DateTimeField()
    orders = models.ManyToManyField(Order)
    comment_type = models.CharField(max_length=255,default='comment')
    label = models.CharField(max_length=255,default="")
    prev = models.CharField(max_length=255, default="")
    new = models.CharField(max_length=255, default="")
    place = models.CharField(max_length=255, default="")
    identification = models.CharField(max_length=255, default="")


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
    photo = models.TextField(default='')
    orders = models.ManyToManyField(Order)
    comments = models.ManyToManyField(Comment)
    last_notifications = models.DateTimeField('дата последнего уведомления', default=timezone.now)
    next_notifications = models.DateTimeField('дата последнего уведомления', default=timezone.now)
    notifications = models.BooleanField('отрпавлять уведомления?', default=True)

    def __str__(self):
        return f'Изделие "{self.name}" связано с {len(self.orders.all())} заказами'

    def payments_result(self):
        payments = self.payment_set.all()
        order_table = list()
        order_report = {
            'Стоимость для клиента': Decimal(0.00),
            'Предоплата':Decimal(0.00),
            'Остаток':Decimal(0.00),
            'Доход':Decimal(0.00),
            'Расход':Decimal(0.00),
            'Прибыль':Decimal(0.00),
            'Наценка':Decimal(0.00),
            'Прибыль в %':0,
            'Длительность': 0,
            'Прибыль в день':Decimal(0.00),
        }
        for payment in payments:
            if payment.type_operation == 'predoplata':
                order_report['Остаток'] -= payment.my_count
                order_report['Предоплата'] += payment.my_count
                order_report['Доход'] += payment.my_count
            elif payment.type_operation == 'rabota':
                order_report['Доход'] += payment.my_count
                order_report['Остаток'] += payment.my_count

            elif payment.type_operation == 'dohod':
                order_report['Остаток'] -= payment.my_count
                order_report['Стоимость для клиента'] += payment.my_count
            elif payment.type_operation == 'rashod':
                order_report['Остаток'] += payment.client_count
                order_report['Стоимость для клиента'] += payment.client_count
                order_report['Доход'] += payment.client_count-payment.my_count
                order_report['Расход'] += payment.my_count
                order_report['Наценка'] += payment.client_count-payment.my_count

        order_report['Прибыль'] += order_report['Доход'] - order_report['Расход']
        if order_report['Расход']:
            order_report['Прибыль в %'] += round(((order_report['Прибыль'] * 100) / order_report['Расход']),2)
        else:
            order_report['Прибыль в %'] = 0
        order_report['Длительность'] = (self.complete_date - self.create_date).days
        if order_report['Длительность']:
            order_report['Прибыль в день'] = round((order_report['Прибыль']/order_report['Длительность']),2)
        else:
            order_report['Прибыль в день'] = 0

        for k,v in order_report.items():
            if k in ['Стоимость для клиента','Предоплата','Остаток','Доход', 'Расход','Прибыль','Наценка', 'Прибыль в день']:
                order_report[k] =str(order_report[k])+'\xa0₽'
            if k in ['Прибыль в %']:
                order_report[k] = str(order_report[k]) + '\xa0%'
            if k in ['Длительность']:
                order_report[k] = str(order_report[k]) + '\xa0дней'
        return order_report


class Payment(models.Model):
    name = models.CharField(max_length=255)
    my_count = models.DecimalField(max_digits=65, decimal_places=2)
    client_count = models.DecimalField(max_digits=65, decimal_places=2)
    type_operation = models.CharField(max_length=25)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True,null=True)
