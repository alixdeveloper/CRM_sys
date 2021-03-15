from telegram_bot.views import bot
from telebot import TeleBot, types
from django.db.models import Q
from main.models import Product
import datetime
from django.utils import timezone
import json
import requests


def update_something():
    requests.get('<URL>')
    products = Product.objects.filter(~Q(status='Закрыт'))  # Находим все незакрытые заказы
    for product in products:
        if product.notifications and (product.complete_date-timezone.now()) < datetime.timedelta(days=7) and product.next_notifications < timezone.now():
            if product.complete_date - product.last_notifications < datetime.timedelta(days=7) and product.complete_date - product.last_notifications > datetime.timedelta(days=3):
                send_notification(order=product.orders.first().id, product=product.id)
                product.last_notifications = timezone.now()
                product.save()
            elif product.complete_date - product.last_notifications > datetime.timedelta(days=3): # если последнее уведомление было за 3 дня: # если последнее уведомление было за 7 дней
                send_notification(order=product.orders.first().id, product=product.id)
                product.last_notifications = timezone.now()
                product.save()
            elif product.next_notifications > product.last_notifications and timezone.now()> product.next_notifications:
                send_notification(order=product.orders.first().id, product=product.id)
                product.last_notifications = timezone.now()
                product.save()


def send_notification(order, product):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Напомнить позже', callback_data=json.dumps({'action':'time','time': 15, 'order': order, 'product': product}))
    button2 = types.InlineKeyboardButton(text='Открыть в CRM', callback_data='open', url=f"https://vantsov.ru/order/{order}?product={product}")  # ex.https://vantsov.ru/order/1?product=1
    button3 = types.InlineKeyboardButton(text='Ок', callback_data=json.dumps({'action': 'close', 'time': 15, 'order': order, 'product': product}))
    keyboard.add(button1,button2,button3)
    bot.send_message('<ID>', text='Напоминание', reply_markup=keyboard)
