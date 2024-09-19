from django.db import models
from account.models import NightDimondUser
from store.models import Product
# Create your models here.


class ReturnedItem(models.Model):
    status = models.CharField(
        max_length=20,
        choices=[('در انتظار', 'در انتظار'),
                 ('تایید شده', 'تایید شده'),
                 ('رد شده', 'رد شده'),],
        default='در انتظار'
    )

    user = models.ForeignKey(NightDimondUser, on_delete=models.SET_NULL, null=True, related_name='returned_item')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='return_request')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.product.name} by {self.user.phone}'


class ReturnImage(models.Model):
    return_item = models.ForeignKey(ReturnedItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='return-images/')

    def __str__(self):
        return f'image for {self.return_item}'
