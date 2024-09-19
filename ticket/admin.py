from django.contrib import admin
from .models import Ticket, Message
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'description', 'created_at', 'updated_at', 'status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'content', 'timestamp', 'is_admin']
