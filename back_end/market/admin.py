from django.contrib import admin
from market.models import Account, Products, Cart


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'first_name', 'last_name', 'address', 'role')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('vendor_code', 'name', 'purchase_price', 'sale_price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'number', 'price', 'total')


admin.site.register(Account, AccountAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart, CartAdmin)
