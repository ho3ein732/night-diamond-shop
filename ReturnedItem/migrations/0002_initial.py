# Generated by Django 5.0.7 on 2024-09-19 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ReturnedItem', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='returneditem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='return_request', to='store.product'),
        ),
        migrations.AddField(
            model_name='returneditem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='returned_item', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='returnimage',
            name='return_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ReturnedItem.returneditem'),
        ),
    ]
