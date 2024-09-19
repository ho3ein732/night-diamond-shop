from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message , Ticket
from .forms import TicketForm, MessageForm
# Create your views here.


def list_tickets(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'ticket/list.html', {'tickets': tickets})


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket:tickets')
    else:
        form = TicketForm()
    return render(request, 'ticket/create.html', {'form': form})


def detail_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("شما اجازه دسترسی به این تیکت را ندارید.")

    messages = ticket.messages.all().order_by('timestamp')

    ticket_message = {
        'content': ticket.description,
        'sender': ticket.user,
        'timestamp': ticket.created_at
    }
    messages = [ticket_message] + list(messages)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ticket = ticket
            message.sender = request.user
            message.is_admin = False
            message.save()
            return redirect('ticket:detail_ticket', ticket_id=ticket.id)
    else:
        form = MessageForm()

    return render(request, 'ticket/detail.html', {'ticket': ticket, 'messages': messages, 'form': form,
                                                  'is_closed': ticket.status == 'closed'})



