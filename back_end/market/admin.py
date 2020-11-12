from django.contrib import admin
from .models import CustomUser, Products, Cart, Order


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'second_name',
                    'middle_name', 'address', 'role')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor_code', 'name',
                    'purchase_price', 'sale_price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'number', 'price', 'total', 'order')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'dest_address', 'total')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
