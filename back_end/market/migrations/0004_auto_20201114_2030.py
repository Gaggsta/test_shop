# Generated by Django 3.1.3 on 2020-11-14 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_order_client'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('client', 'product', 'order')},
        ),
    ]