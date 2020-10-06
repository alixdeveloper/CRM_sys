from django.shortcuts import render
import telebot
from django.conf import settings
from django.views import View
from telebot import TeleBot, types, logger
from django.http import HttpResponse
bot = telebot.TeleBot(settings.NOTIFICATION_TOKEN)


class UpdateBot(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Бот запусчен и работает.")

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return HttpResponse({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    text = 'Тест'
    bot.send_message(message.chat.id, text=text)


