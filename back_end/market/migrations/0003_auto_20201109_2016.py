# Generated by Django 3.1.3 on 2020-11-09 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0002_auto_20201109_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='account',
            name='address',
            field=models.CharField(max_length=500, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='account',
            name='middle_name',
            field=models.CharField(max_length=30, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('Клиент', 'клиент'), ('Менеджер', 'менеджер')], max_length=8, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Эл. почта'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.account', verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Цена за ед.'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.products', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Сумма по строке'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='products',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Закуп. цена'),
        ),
        migrations.AlterField(
            model_name='products',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Розн. цена'),
        ),
        migrations.AlterField(
            model_name='products',
            name='vendor_code',
            field=models.CharField(max_length=15, verbose_name='Артикул'),
        ),
    ]
