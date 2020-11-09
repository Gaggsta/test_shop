# Generated by Django 3.1.3 on 2020-11-09 16:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=500)),
                ('role', models.CharField(choices=[('Клиент', 'клиент'), ('Менеджер', 'менеджер')], max_length=8)),
                ('user_email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=100)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.account')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.products')),
            ],
        ),
    ]
