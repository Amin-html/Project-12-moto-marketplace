from rest_framework import serializers
from .models import Cart, CartItem
from catalog.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    # source='product' — говорит DRF взять для этого поля значение
    # из product (реального ForeignKey), просто отдать его под другим
    # именем и в развёрнутом виде через ProductSerializer
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']