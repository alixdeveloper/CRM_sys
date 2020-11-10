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
    path('delete', views.detele_data, name='delete_data'),
    path('create_comment_order', views.create_comment_order, name='create_comment_order'),
    path('create_comment_product', views.create_comment_product, name='create_comment_product'),
    path('change_order_info', views.change_order_info, name='change_order_info'),
    path('change_client_info', views.change_client_info, name='change_client_info'),
    path('change_product_info', views.change_product_info, name='change_product_info'),
    path('change_product_status', views.change_product_status, name='change_product_status'),
    path('change_order_status', views.change_order_status, name='change_order_status'),
    path('link_product_to_order', views.link_product_to_order, name='link_product_to_order'),
    #
    path('order/<int:order_id>/', views.order, name='order'),
    path('status', views.status, name='status'),
    path('login', views.login, name='login'),
    path('search', views.search, name='search'),
    path('logout', views.logout, name='logout'),

    # path('client', views.client, name='client'),
    # path('product', views.product, name='product'),
]