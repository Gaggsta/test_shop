from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    USER_ROLES = (
        ("Клиент", "клиент"), ("Менеджер", "менеджер")
    )
    user_email = models.OneToOneField(
        User, verbose_name='Эл. почта', on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    middle_name = models.CharField(
        verbose_name='Отчество', max_length=30, null=True)
    address = models.CharField(verbose_name='Адрес', max_length=500)
    role = models.CharField(verbose_name='Роль',
                            max_length=8, choices=USER_ROLES)

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Products(models.Model):
    vendor_code = models.CharField(verbose_name='Артикул', max_length=15)
    name = models.CharField(verbose_name='Название', max_length=100)
    purchase_price = models.DecimalField(
        verbose_name='Закуп. цена', max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(
        verbose_name='Розн. цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.vendor_code

    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)
        changes = Cart.objects.filter(product=self)
        for change in changes:
            change.save()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    # Корзина: клиент, товар, количество, цена, сумма по строке.
    client = models.ForeignKey(
        Account, verbose_name='Покупатель', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Products, verbose_name='Товар', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(
        'Количество', validators=[MinValueValidator(1)])
    price = models.DecimalField(
        verbose_name='Цена за ед.', max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(
        verbose_name='Сумма по строке', max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.client}  {self.product}'

    def save(self, *args, **kwargs):
        self.price = self.product.sale_price
        self.total = self.price * self.number
        super(Cart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
