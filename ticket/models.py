from django.db import models
from account.models import NightDimondUser
# Create your models here.


class Ticket(models.Model):
    Status =(
        ('open', 'open'),
        ('in_progress', 'in_progress'),
        ('closed', 'closed'),
    )
    user = models.ForeignKey(NightDimondUser, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status, default='open')

    def __str__(self):
        return self.subject


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(NightDimondUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'User message from {self.sender.first_name} at {self.timestamp}'


