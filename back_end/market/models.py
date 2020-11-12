from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Profile(models.Model):
    USER_ROLES = (
        ("клиент", "Клиент"), ("менеджер", "Менеджер")
    )
    user_email = models.OneToOneField(
        User, verbose_name='Эл. почта', on_delete=models.CASCADE)

    middle_name = models.CharField(
        verbose_name='Отчество', max_length=30, null=True)
    address = models.CharField(verbose_name='Адрес', max_length=500)
    role = models.CharField(verbose_name='Роль',
                            max_length=8, choices=USER_ROLES, default=("Клиент", "клиент"))

    def first_name(self):
        return self.user_email.first_name
    first_name.null = True
    first_name.default = '-'
    first_name.short_description = 'Имя'

    def last_name(self):
        return self.user_email.last_name
    first_name.null = True
    last_name.default = '-'
    last_name.short_description = 'Фамилия'

    def __str__(self):
        return f'{self.user_email.first_name}  {self.user_email.last_name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


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
    def client(self):
        cart = Cart.objects.filter(order=self)[0]
        return cart.client

    def dest_address(self):
        cart = Cart.objects.filter(order=self)[0]
        return cart.client.address
    dest_address.short_description = 'Адрес доставки'

    def total(self):
        carts = Cart.objects.filter(order=self)
        total_sum = 0
        for product in carts:
            total_sum = total_sum + product.total()
        return total_sum
    total.default = 0
    total.short_description = 'Сумма по заказу'

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Cart(models.Model):
    # Корзина: клиент, товар, количество, цена, сумма по строке.
    client = models.ForeignKey(
        Profile, verbose_name='Покупатель', on_delete=models.CASCADE)
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
        unique_together = ('client', 'product')
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
