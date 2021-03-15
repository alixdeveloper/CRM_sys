from django.shortcuts import render
import telebot
from django.conf import settings
from django.views import View
from telebot import TeleBot, types, logger
from django.http import HttpResponse
import json
from main.models import Product
from django.utils import timezone
import datetime
bot = telebot.TeleBot(settings.NOTIFICATION_TOKEN)


class UpdateBot(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Бот запущен и работает.")

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return HttpResponse({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Напомнить позже', callback_data=json.dumps({'action':'time','time': 15, 'order': 1, 'product': 1}))
    button2 = types.InlineKeyboardButton(text='Открыть в CRM', callback_data='open', url=f"https://vantsov.ru/order/1?product=1")  # ex.https://vantsov.ru/order/1?product=1
    button3 = types.InlineKeyboardButton(text='Ок', callback_data=json.dumps({'action': 'close', 'time': 15, 'order': 1, 'product': 1}))
    keyboard.add(button1,button2,button3)
    bot.send_message(message.chat.id, text='Напоминание', reply_markup=keyboard) # Me


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.message:
        data = json.loads(call.data)
        time, product, order = data['time'], data['product'], data['order']
        product = Product.objects.get(id=product)
        if data['action'] == 'close':
            # product.notifications = False
            # product.save()
            bot.answer_callback_query(callback_query_id=call.id, text='Напоминаний больше не будет')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Напоминаний больше не будет")

        elif data['action'] == 'time':
            # product.next_notifications = timezone.now() + datetime.timedelta(minutes=15)
            # product.save()
            bot.answer_callback_query(callback_query_id=call.id, text='Напомню через 15 минут')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Напомню через 15 минут")

