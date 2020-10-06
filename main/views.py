from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from django.utils.dateparse import parse_date
from django.utils import timezone
from .models import Order, Client, Product, Comment, Payment
import uuid, os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import hashlib
from django.conf import settings
import collections
import hashlib
import hmac

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
        return HttpResponseRedirect('login')
    orders = Order.objects.all()
    return render(request, 'main/index.html', {'orders':orders, 'theme':request.session.get('theme','light')})


def order(request, order_id):
    if not request.session.get('login', False):
        return HttpResponseRedirect('login')

    request.session['last_order'] = order_id
    request.session.modified = True
    _order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        message = request.POST['comment']
        date = timezone.now()
        comment = Comment(message=message, date=date, order=_order)
        comment.save()
        comments = Comment.objects.filter(order=_order)
        return HttpResponseRedirect(reverse('main:order',kwargs={'order_id':order_id}))
    else:
        comments = Comment.objects.filter(order=_order)
        clients = Client.objects.all()
        products = Product.objects.all()
        payments = _order.payment_set.all()
        return render(request, 'main/order.html', {'payments': payments, 'comments': comments, 'order': _order, 'clients': clients, 'products': products, 'theme':request.session.get('theme','light')})


def link_product_to_order(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('login')

    if request.POST.get('save', False):
        order = Order.objects.get(id=request.POST['order'])
        product = Product.objects.get(name=request.POST['product'])
        product.orders.add(order)
        product.save()
        return HttpResponseRedirect(f'/order/{order.id}')


def create_order(request):
    if not request.session.get('login', False):
        return HttpResponseRedirect('login')

    if request.method == "POST":
        name = request.POST.get('name', '') or ''
        create_date = parse_date(request.POST['create_date'])
        complete_date= parse_date(request.POST['complete_date'])
        weight = float(request.POST.get('weight', 0) or 0)
        preorder_weight = float(request.POST.get('preorder_weight', 0) or 0)
        price = float(request.POST.get('price', 0) or 0)
        prepayment = float(request.POST.get('prepayment', 0) or 0)
        ads = request.POST.get('ads','')
        order = Order(name=name,create_date=create_date,complete_date=complete_date,
                      weight=weight,price=price,prepayment=prepayment,ads=ads, preorder_weight=preorder_weight)
        order.save()
        comment = request.POST.get('comment', '')
        if comment:
            date = timezone.now()
            comment = Comment(message=comment, date=date, order=order)
            comment.save()

        return HttpResponseRedirect(reverse('main:index'))
    else:
        return render(request, 'main/create_order.html',{ 'theme':request.session.get('theme','light')})


def create_payment(request):
    if request.method == 'POST':
        description = request.POST['description']
        my_price = request.POST['my_price']

        type_operation = request.POST['options']
        if type_operation == '-':
            three = request.POST['three']
            payment = Payment(name=description, my_price=my_price, client_price=three, type_operation='-')
            last_order = request.session['last_order']
            payment.save()
            payment.orders.add(Order.objects.get(id=last_order))
            payment.save()
            return HttpResponseRedirect(f'order/{last_order}')
        elif type_operation == '+':
            ...
        elif type_operation == '=':
            ...
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
        return HttpResponseRedirect('login')

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
        return HttpResponseRedirect('login')

    # return HttpResponse(f'{os.path.dirname(os.path.realpath(__file__))}/static/main/uploads/image/')
    if request.method == 'POST':
        name = request.POST['name']
        material = request.POST['material']
        color = request.POST['color']
        weight = float(request.POST.get('weight', 0) or 0)
        length = float(request.POST.get('length', 0) or 0)
        width = float(request.POST.get('width', 0) or 0)
        height = float(request.POST.get('height', 0) or 0)
        size = float(request.POST.get('size', 0) or 0)
        photo_name = str(uuid.uuid4())
        if request.FILES.get('photo', False):
            photo = request.FILES['photo']
            photo_name = photo_name+"."+photo.name.split(".")[-1]
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/static/main/uploads/image/{photo_name}', 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)

        else:
            photo_name = ''
        last_order = request.session['last_order']
        product = Product(name=name,material=material,color=color,weight=weight,
                          length=length,width=width,height=height,size=size,photo=photo_name)
        product.save()
        product.orders.add(Order.objects.get(id=last_order))
        product.save()
        return HttpResponseRedirect(f'order/{last_order}')

    else:
        return render(request, 'main/create_product.html',{ 'theme':request.session.get('theme','light')})


def login(request):

    # request.session['login'] = True

    username = request.GET.get('username', None)
    data = {k: str(request.GET[k]) for k in request.GET}
    if username in ['plisovalix', 'Vantsov'] and check_integrity(settings.TELEGRAM_TOKEN, data):
        request.session['login'] = True
        return HttpResponseRedirect('/')

    return render(request,'main/login_page.html', {'theme':request.session.get('theme','light')})


def logout(request):
    request.session['login'] = False
    return HttpResponseRedirect('login')
