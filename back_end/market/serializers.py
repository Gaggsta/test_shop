from rest_framework import serializers
from .models import Cart, Order


class CertSerializer(serializers.ModelSerializer):
    """
    List of goods by cart

    """
    class Meta:
        model = Cart
        fields = ('client', 'product', 'number', 'price', 'total')


class OrderSerializer(serializers.ModelSerializer):
    """
    Show order
    """
    class Meta:
        model = Order
        fields = ('id', 'client', 'dest_address', 'total')
