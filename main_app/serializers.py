from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Order
        fields = ('id', 'qr_code')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Store
        fields = ('id', 'name', 'email')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Product
        fields = ('id', 'img', 'name', 'price')
