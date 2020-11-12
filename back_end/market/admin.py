from django.contrib import admin
from .models import Profile, Products, Cart, Order


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'first_name', 'last_name', 'middle_name',
                    'address', 'role')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor_code', 'name',
                    'purchase_price', 'sale_price')


class CartAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'number', 'price', 'total', 'order')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'dest_address', 'total')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
