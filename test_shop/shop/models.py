from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    name = models.CharField("Название бренда", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Бренды")


class Images(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(
        Product, verbose_name="Относится к товару", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Изображения")


class Product(models.Model):
    name = models.CharField("Название", max_length=100)
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.SET_NULL)
    info = models.TextField("Описание товара",)
    price = models.DecimalField("Цена", decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Товары")
