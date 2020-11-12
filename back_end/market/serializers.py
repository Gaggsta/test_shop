from rest_framework import serializers
from .models import Cart, Profile


class CertSerializer(serializers.ModelSerializer):
    """
    List of goods by cart

    """
    class Meta:
        model = Cart
        fields = ('client', 'product', 'number', 'price', 'total')
