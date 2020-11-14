
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from telegram_bot.views import UpdateBot
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path(settings.NOTIFICATION_TOKEN, csrf_exempt(UpdateBot.as_view()), name='update'),
]
