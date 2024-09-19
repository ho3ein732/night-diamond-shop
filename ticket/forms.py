from django import forms
from .models import Message, Ticket


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description']

