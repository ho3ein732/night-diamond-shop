from django.db import models
from account.models import NightDimondUser
from store.models import Product
# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(NightDimondUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    detailed_address = models.TextField()
    postal_code = models.CharField(max_length=11)
    plaque = models.CharField(max_length=10)
    recipient_phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.phone} -> {self.detailed_address}'

# Orders


class Order(models.Model):

    class Status(models.TextChoices):
        ORDER_CONFIRMATION = 'تایید سفارش', "تایید سفارش"
        review_queue = 'در صف بررسی', "در صف بررسی"
        preparation = 'آماده‌سازی', "آماده‌سازی"
        Delivery_to_post = 'تحویل به پست', "تحویل به پست"

    buyer = models.ForeignKey(NightDimondUser, on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='address')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.ORDER_CONFIRMATION)

    class Meta:
        ordering = ['-updated']
        indexes = [
            models.Index(fields=['-updated'])
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum([item.get_cost() for item in self.items.all()])

    def get_post_cost(self):
        weight = sum([item.get_weight() for item in self.items.all()])
        if weight < 1000:
            return 50000
        else:
            return 150000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()


class OrderItem(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} * {self.quantity}'

    def get_cost(self):
        return self.quantity * self.price

    def get_weight(self):
        return self.quantity * self.weight