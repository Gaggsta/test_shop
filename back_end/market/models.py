from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .managers import CustomUserManager
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
        ("клиент", "Клиент"), ("менеджер", "Менеджер")
    )
    email = models.EmailField('email', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(
        verbose_name='Имя', max_length=30, null=True)
    second_name = models.CharField(
        verbose_name='Фамилия', max_length=30, null=True)
    middle_name = models.CharField(
        verbose_name='Отчество', max_length=30, null=True)
    address = models.CharField(verbose_name='Адрес', max_length=500)
    role = models.CharField(verbose_name='Роль',
                            max_length=30, choices=USER_ROLES, default=("Клиент", "клиент"))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

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

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Покупатель', on_delete=models.CASCADE)

    def dest_address(self):
        return self.client.address

    dest_address.short_description = 'Адрес доставки'

    def total(self):
        carts = Cart.objects.filter(order=self)
        total_sum = 0
        for product in carts:
            total_sum = total_sum + product.total()
        return total_sum
    total.default = 0
    total.short_description = 'Сумма по заказу'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        cart = Cart.objects.filter(
            client=self.client).exclude(order__isnull=False)

        for product in cart:
            product.order = self
            product.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Cart(models.Model):
    # Корзина: клиент, товар, количество, цена, сумма по строке.
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Покупатель', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Products, verbose_name='Товар', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(
        'Количество', validators=[MinValueValidator(1)])
    order = models.ForeignKey(
        Order, verbose_name='Заказ', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.client}  {self.product}'

    def price(self):
        return self.product.sale_price
    price.default = 0
    price.short_description = 'Цена за ед.'

    def total(self):
        return self.product.sale_price * self.number
    total.default = 0
    total.short_description = 'Сумма по строке'

    class Meta:
        unique_together = ('client', 'product', 'order')
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
