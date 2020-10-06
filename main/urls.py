from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls import url

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_order', views.create_order, name='create_order'),
    path('create_client', views.create_client, name='create_client'),
    path('create_product', views.create_product, name='create_product'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('link_product_to_order', views.link_product_to_order, name='link_product_to_order'),
    #
    path('order/<int:order_id>/', views.order, name='order'),
    path('status', views.status, name='status'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # path('client', views.client, name='client'),
    # path('product', views.product, name='product'),
]