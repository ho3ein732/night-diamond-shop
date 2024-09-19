import random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .forms import *
from .models import NightDimondUser
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from cart.models import Order
from cart.cart import Cart
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def verify_phone(request):
    # if request.user.is_authenticated():
    #     return redirect('account:login') # تکمیل شود
    # else:
    if request.method == 'POST':
        form = UserCreatedForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password1']
            if NightDimondUser.objects.filter(phone=phone).exists():
                messages.error(request, 'شما قبلا ثبت نام کردید وارد شوید.')
                return redirect('account:login')  # تکمیل شود
            else:
                token = ''.join(random.choices('1234567890', k=6))
                cache.set(phone, token, timeout=300)
                subject = 'تولیدی الــماس شب | کد تایید'
                message = 'کد تایید شما : ' + token
                send_mail(subject, message, 'ho3ein.732h@gmail.com',
                          ['ho33ein.732h@gmail.com', 'alikjfilejejl@gmail.com'],
                          fail_silently=False)
                request.session['phone'] = phone
                request.session['password'] = password
                return redirect('account:verify-code')
    else:
        form = UserCreatedForm()
    return render(request, 'verify/verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            phone = request.session.get('phone')
            cache_token = cache.get(phone)
            if token == cache_token:
                password = request.session['password']
                user = NightDimondUser.objects.create(phone=phone, password=password)
                login(request, user)
                messages.success(request, 'ثبت نام با موفقیت انجام شد.')
                return redirect('store:products')
            else:
                messages.error(request, 'کد تایید اشتباه است.')
    else:
        form = VerifyCodeForm()
    return render(request, 'verify/verify_token.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('store:products')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('store:products')


@login_required
def profile(request):
    user = request.user

    return render(request, 'account/profile.html', {'user': user})


@login_required
def edite_account_information(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return HttpResponse('?updated=true')
    return render(request, 'account/edite-account-information.html', {'user': user})


@login_required
def verify_new_phone(request):
    if request.method == 'POST':
        form = NewPhoneForm(data=request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if NightDimondUser.objects.filter(phone=phone).exists():
                messages.error(request, 'این شماره تلفن قبلا ثبت شده')
            else:
                token = ''.join(random.choices('1234567890', k=6))
                cache.set(phone, token, timeout=180)
                subject = 'تولیدی الــماس شب | کد تایید شما '
                message = 'کد تایید شما : ' + token
                send_mail(subject, message, 'ho3ein.732h@gmail.com',
                          ['ho33ein.732h@gmail.com', 'alikjfilejejl@gmail.com'],
                          fail_silently=False)
                request.session['phone'] = phone
                return redirect('account:verify-new-phone_code')
    else:
        form = NewPhoneForm()
    return render(request, 'verify/verify-new-phone.html', {'form': form})


@login_required
def verify_new_phone_code(request):
    if request.method == 'POST':
        form = VerifyCodeForm(data=request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            phone = request.session.get('phone')
            cache_token = cache.get(phone)
            if token == cache_token:
                user = request.user
                user.phone = phone
                user.save()

                return redirect('account:profile')
            else:
                messages.error(request, 'کلمه عبور اشتباه است')
    else:
        form = VerifyCodeForm()
    return render(request, 'verify/verify_token.html', {'form': form})

