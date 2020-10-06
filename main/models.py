from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=255)
    create_date = models.DateTimeField('дата приема заказа')
    complete_date = models.DateTimeField('дата завершения заказа')
    weight = models.FloatField(default=0)
    preorder_weight = models.FloatField(default=0)
    price = models.FloatField(default=0)
    prepayment = models.FloatField(default=0)
    comment = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='new')
    ads = models.CharField(max_length=255)


    def __str__(self):
        return f'Заказ {self.id} от {self.create_date}'


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
    material = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    size = models.FloatField(default=0)
    photo = models.CharField(max_length=255)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f'Изделие "{self.name}" связано с {len(self.orders.all())} заказами'


class Comment(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')


class Payment(models.Model):
    name = models.CharField(max_length=255)
    my_price = models.CharField(max_length=255)
    client_price = models.CharField(max_length=255)
    type_operation = models.CharField(max_length=255)
    orders = models.ManyToManyField(Order)
