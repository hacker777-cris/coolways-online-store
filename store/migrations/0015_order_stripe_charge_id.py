# Generated by Django 4.2.1 on 2023-07-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_order_delivery_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]