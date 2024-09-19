from django.contrib import admin
from .models import *
# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class FeaturesInline(admin.TabularInline):
    model = ProductFeatures
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'slug', 'description', 'category',
        'price', 'new_price', 'inventory', 'off',
        'created', 'updated'
    ]

    inlines = [FeaturesInline, ImageInline]
    prepopulated_fields = {'slug': ('name',)}  # پر کردن خودکار اسلاگ


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # پر کردن خودکار اسلاگ


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']