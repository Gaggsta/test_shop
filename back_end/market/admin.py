from django.contrib import admin
from .models import CustomUser, Products, Cart, Order
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'second_name',
                    'middle_name', 'address', 'role')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'second_name',
                           'middle_name', 'address', 'role')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'second_name',
                       'middle_name', 'address', 'role', 'password1', 'password2', )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


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
