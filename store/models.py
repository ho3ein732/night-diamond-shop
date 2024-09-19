from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField
from django.utils.text import slugify
from account.models import NightDimondUser


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return f'category {self.name}'

    class Meta:
        ordering = ['-name']
        indexes = [
            models.Index(fields=['name', 'slug'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    inventory = models.IntegerField(default=0)
    weight = models.PositiveIntegerField(default=0)
    off = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} product with a price of {self.new_price}'

    class Meta:
        ordering = ['-created']

        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['created', 'updated']),
            models.Index(fields=['name'])
        ]
        verbose_name = 'مجصول'
        verbose_name_plural = 'محصولات'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:post_detail', args=[self.id, self.slug])


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    file = ResizedImageField(verbose_name='عکس ها', upload_to='images/', size=[500, 500],
                             crop=['middle', 'center'], force_format='PNG', quality=100)
    title = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'photo for {self.product.name} product'

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])
        ]


class ProductFeatures(models.Model):
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
    features = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')


class FavoriteProduct(models.Model):
    user = models.ForeignKey(NightDimondUser, on_delete=models.CASCADE, verbose_name='favorite_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} saved the {self.product.name}'

