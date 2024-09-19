from . import views
from django.urls import path

app_name = 'ticket'

urlpatterns = [
    path('list/', views.list_tickets, name='tickets'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('datail/<int:ticket_id>/', views.detail_ticket, name='detail_ticket')
]