from django.urls import path, include
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart Urls
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('updateQuantity', views.update_quantity, name='update_quantity'),
    path('removeItem/', views.remove_item, name='remove_item'),

    # Address Urls

    path('load-cities/', views.load_cities, name='load_cities'),
    path('add-address/', views.add_address, name='add_address'),

    # Orders Urls

    path('order-list/', views.order_list, name='order_list'),
    path('order-detail/<int:id>/', views.order_detail, name='order_detail')
]