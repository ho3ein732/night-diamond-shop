from django.urls import path, include
from . import views

app_name = 'ReturnedItem'

urlpatterns = [
    # create
    path('create-returned-item/<int:user_id>/<int:product_id>/', views.create_returned_item, name='create-returned-item'),
    # list
    path('list-returned-goods/', views.list_returned_goods, name='list-returned-goods'),
    # detail
    path('details-returned-goods/<int:item_id>/', views.details_returned_goods, name='details-returned-goods'),


]