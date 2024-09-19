from django.contrib import admin
from .models import NightDimondUser
from django.contrib.auth.admin import UserAdmin
from .forms import *


@admin.register(NightDimondUser)
class NightDimondUserAdmin(UserAdmin):  # تغییر به UserAdmin
    ordering = ['phone']
    model = NightDimondUser
    add_form = NightDimondUserCreationForm  # اصلاح اشتباه تایپی
    form = NightDimondUserChangeForm
    list_display = ['id', 'phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )