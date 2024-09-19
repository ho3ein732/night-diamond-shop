from django.contrib import admin
from .models import ReturnedItem, ReturnImage


# Register your models here.


class ReturnImageInline(admin.TabularInline):
    model = ReturnImage
    extra = 0


@admin.register(ReturnedItem)
class ReturnedItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product',
                    'reason', 'created_at',
                    'email', 'phone']
    inlines = [ReturnImageInline]
