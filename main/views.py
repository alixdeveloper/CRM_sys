import pytz
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from django.utils.dateparse import parse_date
from django.utils import timezone
from .models import Order, Client, Product, Comment, Payment, ProductCategory
import uuid, os
from django.http import JsonResponse
from main.templatetags import parse_iso_order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import hashlib
from decimal import Decimal
from django.conf import settings
import collections
import hashlib
import hmac
from datetime import datetime
import json

def new_comment(request,comment_type, prev, new, place, identification ):
    timezone.activate(pytz.timezone("Europe/Moscow"))
    date = timezone.now()
    order_id = request.session['last_order']
    _order = get_object_or_404(Order, pk=order_id)
    comment = Comment(date=date,
                      comment_type=comment_type,
                      prev=prev, new=new,
                      place=place, identification=identification)
    comment.save()
    comment.orders.add(_order)
    comment.save()


def check_signature(token: str, hash: str, **kwargs) -> bool:
    """
    Generate hexadecimal representation
    of the HMAC-SHA-256 signature of the data-check-string
    with the SHA256 hash of the bot's token used as a secret key
    :param token:
    :param hash:
    :param kwargs: all params received on auth
    :return:
    """
    secret = hashlib.sha256(token.encode('utf-8'))
    check_string = '\n'.join(map(lambda k: f'{k}={kwargs[k]}', sorted(kwargs)))
    hmac_string = hmac.new(secret.digest(), check_string.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    return hmac_string == hash


def check_integrity(token: str, data: dict) -> bool:
    """
    Verify the authentication and the integrity
    of the data received on user's auth
    :param token: Bot's token
    :param data: all data that came on auth
    :return:
    """
    return check_signature(token, **data)


def index(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')
    orders = Order.objects.all()
    return render(request, 'main/index.html', {'orders':orders, 'theme':request.session.get('theme','light')})


def create_comment_order(request):
    if request.method == "POST":
        order_id= request.session['last_order']
        _order = get_object_or_404(Order, pk=order_id)
        message = request.POST['comment']
        date = timezone.now()
        comment = Comment(message=message, date=date)
        comment.save()
        comment.orders.add(_order)
        comment.save()
        timezone.activate(pytz.timezone("Europe/Moscow"))
        return JsonResponse({'id': comment.id, 'message': comment.message,'date': parse_iso_order.parse_iso_order(timezone.localtime(comment.date))})


def create_comment_product(request):
    if request.method == "POST":
        order_id= request.session['last_order']
        _order = get_object_or_404(Order, pk=order_id)
        message = request.POST['comment']
        comment_type = request.POST['product_id']
        date = timezone.now()
        comment = Comment(message=message, date=date, comment_type=comment_type)
        comment.save()
        comment.orders.add(_order)
        comment.save()
        timezone.activate(pytz.timezone("Europe/Moscow"))
        return JsonResponse({'id': comment.id, 'message': comment.message,'date': parse_iso_order.parse_iso_order(timezone.localtime(comment.date))})


def order(request, order_id):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')
    request.session['last_order'] = order_id
    request.session.modified = True
    _order = get_object_or_404(Order, pk=order_id)
    comments = _order.comment_set.all()
    comments_product = _order.comment_set.all()
    comments_product = [x for x in comments_product if x.comment_type.isdigit() or x.comment_type == 'product']
    clients = _order.client_set.all()
    products = _order.product_set.all()
    payments = _order.payment_set.all()
    payments_result = _order.payments_result()
    return render(request, 'main/order.html', {'payments': payments, 'comments': comments,
                                               'order': _order, 'clients': clients,
                                               'products': products, 'theme':request.session.get('theme','light'),
                                               'order_table': payments_result['order_table'], 'order_report':payments_result['order_report'],
                                               'ProductCategory': ProductCategory.objects.all(),
                                               'comments_product':comments_product,
                                               })


def link_product_to_order(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')

    if request.POST.get('save', False):
        order = Order.objects.get(id=request.POST['order'])
        product = Product.objects.get(name=request.POST['product'])
        product.orders.add(order)
        product.save()
        return HttpResponseRedirect(f'/order/{order.id}')


def change_order_info(request):
    last_order = request.session['last_order']
    _order = Order.objects.get(id=last_order)
    _order.name = request.POST['name']
    _order.create_date = datetime.strptime(request.POST['create_date'], "%Y-%m-%d")
    # _order.complete_date = datetime.strptime(request.POST['complete_date'], "%Y-%m-%d")
    _order.weight = round(Decimal(request.POST['weight']),2)
    # _order.preorder_weight = round(Decimal(request.POST['preorder_weight']),2)
    # _order.price = round(Decimal(request.POST['price']),2)
    # _order.prepayment = round(Decimal(request.POST['prepayment']),2)
    # _order.status = request.POST['status']
    _order.ads = request.POST['ads']
    _order.save()
    new_comment(request, 'info', request.POST['prev'], request.POST['new'], request.POST['place'], request.POST['identification'])
    return JsonResponse({'_order.name': str(_order.create_date)})


def change_client_info(request):
    last_order = request.session['last_order']
    _order = Order.objects.get(id=last_order)
    client = _order.client_set.get(id=request.POST['client_id'])
    client.last_name = request.POST['last_name']
    client.first_name = request.POST['first_name']
    client.middle_name = request.POST['middle_name']
    client.phone = request.POST['phone']
    client.city = request.POST['city']
    client.communication_type = request.POST['communication_type']
    client.save()
    new_comment(request, 'client', request.POST['prev'], request.POST['new'], request.POST['place'], request.POST['identification'])
    return JsonResponse({})


def change_product_info(request):
    last_order = request.session['last_order']
    _order = Order.objects.get(id=last_order)
    product = _order.product_set.get(id=request.POST['product_id'])
    product.size = request.POST['psize']
    product.category = request.POST['category']
    product.complete_date = datetime.strptime(request.POST['complete_date'], "%Y-%m-%d")
    product.height = request.POST['height']
    product.preorder_weight_product = request.POST['preorder_weight_product']
    product.width = request.POST['width']
    product.length = request.POST['length']
    product.weight = request.POST['weight']
    product.color = request.POST['color']
    product.material = request.POST['material']
    product.name = request.POST['name']
    product.save()
    new_comment(request, 'product', request.POST['prev'], request.POST['new'], request.POST['place'], request.POST['identification'])
    return JsonResponse({})


def create_order(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')

    if request.method == "POST":
        name = request.POST.get('name', '') or ''
        create_date = parse_date(request.POST['create_date'])
        # complete_date= parse_date(request.POST['complete_date'])
        weight = float(request.POST.get('weight', 0) or 0)
        preorder_weight = float(request.POST.get('preorder_weight', 0) or 0)
        price = float(request.POST.get('price', 0) or 0)
        # prepayment = float(request.POST.get('prepayment', 0) or 0)
        ads = request.POST.get('ads','')
        order = Order(name=name,create_date=create_date,
                      weight=weight,price=price,ads=ads, preorder_weight=preorder_weight)
        order.save()
        comment = request.POST.get('comment', '')
        if comment:
            date = timezone.now()
            comment = Comment(message=comment, date=date)
            comment.save()
            comment.orders.add(order)
            comment.save()

        return HttpResponseRedirect(reverse('main:index'))
    else:
        return render(request, 'main/create_order.html',{ 'theme':request.session.get('theme','light')})


def detele_data(request):
    data_id = request.POST['data_id']
    data_type = request.POST['data_type']
    if data_type == 'comment':
        comment = Comment.objects.get(id=data_id)
        comment.delete()
        return JsonResponse({'status':'ok'})
    elif data_type == 'payment':
        payment = Payment.objects.get(id=data_id)
        payment.delete()
        return JsonResponse({'status':'ok'})

def change_product_status(request):
    data_id = request.POST['data_id']
    new_status = request.POST['new_status']
    product = Product.objects.get(id=data_id)
    product.status = new_status
    product.save()
    return JsonResponse({'status': 'ok'})


def change_order_status(request):
    data_id = request.POST['data_id']
    new_status = request.POST['new_status']
    _order = Order.objects.get(id=data_id)
    _order.status = new_status
    _order.save()
    return JsonResponse({'status': 'ok'})


def create_payment(request):
    if request.method == 'POST':
        description = request.POST.get('description','')
        my_price = round(Decimal(request.POST.get('my_price','0')),2)
        type_operation = request.POST.get('options')

        if type_operation == '-':
            three = round(Decimal(request.POST.get('three','0')),2)
            payment = Payment(name=description, my_count=my_price, client_count=three, type_operation='-')
            last_order = request.session['last_order']
            payment.save()
            payment.orders.add(Order.objects.get(id=last_order))
            payment.save()
            return JsonResponse({
                'name': payment.name,
                'my_count': payment.my_count,
                'nacenka': payment.client_count-payment.my_count,
                'client_count': payment.client_count,
                'color': '#dc354596'
            })

        elif type_operation == '+':
            payment = Payment(name=description, my_count=my_price, type_operation='+', client_count=0)
            last_order = request.session['last_order']
            payment.save()
            payment.orders.add(Order.objects.get(id=last_order))
            payment.save()
            return JsonResponse({
                'name': payment.name,
                'my_count': payment.my_count,
                'nacenka': 0,
                'client_count': 0,
                'color':'#4fdc3596'
            })
        elif type_operation == '=':
            payment = Payment(name=description, my_count=my_price, client_count=my_price, type_operation='=')
            last_order = request.session['last_order']
            payment.save()
            payment.orders.add(Order.objects.get(id=last_order))
            payment.save()
            return JsonResponse({
                'name': payment.name,
                'my_count': payment.my_count,
                'nacenka': 0,
                'client_count': payment.client_count,
                'color': '#387cff'
            })

        else:
            return HttpResponseRedirect(reverse('main:index'))
    else:
        return HttpResponseRedirect(reverse('main:index'))


def status(request):

    if request.method == 'POST':
        request.session['theme'] = request.POST['theme']
    data = request.session.get('theme','light')
    return HttpResponse(data)


def create_client(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        communication_type = request.POST['communication_type']
        _phone = request.POST['phone']
        phone = ''
        city = request.POST['city']
        for d in str(_phone):
            if d.isdigit():
                phone += d
        if not phone:
            phone = 0
        client = Client(first_name=first_name,last_name=last_name,middle_name=middle_name,
                        phone=phone,city=city, communication_type=communication_type)
        client.save()
        last_order = request.session['last_order']
        client.orders.add(Order.objects.get(id=last_order))
        client.save()
        return HttpResponseRedirect(f'order/{last_order}')
    else:
        return render(request, 'main/create_client.html', {'theme':request.session.get('theme','light')})


def create_product(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')

    # return HttpResponse(f'{os.path.dirname(os.path.realpath(__file__))}/static/main/uploads/image/')
    if request.method == 'POST':
        name = request.POST['name']
        complete_date= parse_date(request.POST['complete_date'])
        category = request.POST['category']
        new_category = request.POST['new_category']
        if new_category:
            new_category_object = ProductCategory(name=new_category)
            new_category_object.save()
            category = request.POST['new_category']

        material = request.POST['material']
        color = request.POST['color']
        weight = float(request.POST.get('weight', 0) or 0)
        preorder_weight = float(request.POST.get('preorder_weight', 0) or 0)

        length = float(request.POST.get('length', 0) or 0)
        width = float(request.POST.get('width', 0) or 0)
        height = float(request.POST.get('height', 0) or 0)
        size = float(request.POST.get('size', 0) or 0)
        photo_list = []
        if request.FILES.get('photo', False):
            photos = request.FILES.getlist('photo')
            for photo in photos:
                photo_name = str(uuid.uuid4())+"."+photo.name.split(".")[-1]
                photo_list.append(photo_name)
                with open(f'{os.path.dirname(os.path.realpath(__file__))}/static/main/uploads/image/{photo_name}', 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

        else:
            photo_name = ''
        last_order = request.session['last_order']
        product = Product(name=name,complete_date=complete_date, category=category, preorder_weight=preorder_weight,material=material,color=color,weight=weight,
                          length=length,width=width,height=height,size=size,photo=json.dumps(photo_list))
        product.save()
        product.orders.add(Order.objects.get(id=last_order))
        product.save()
        return HttpResponseRedirect(f'order/{last_order}')

    else:
        return render(request, 'main/create_product.html',{ 'theme':request.session.get('theme','light'), 'ProductCategory':ProductCategory.objects.all()})


def login(request):

    request.session['login'] = True

    username = request.GET.get('username', None)
    data = {k: str(request.GET[k]) for k in request.GET}
    if username in ['plisovalix', 'Vantsov'] and check_integrity(settings.TELEGRAM_TOKEN, data):
        request.session['login'] = True
        return HttpResponseRedirect('/')

    return render(request,'main/login_page.html',{ 'theme':request.session.get('theme','light')})


def logout(request):
    request.session['login'] = False
    return HttpResponseRedirect('/login')


def search(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('/login')
    data = request.POST.get('data','')
    raw_orders = Order.objects.all()
    orders = []
    for i in raw_orders:
        if data.lower() in i.name.lower():
            orders.append(i)
    return render(request, 'main/index.html', {'orders':orders, 'theme':request.session.get('theme','light')})
