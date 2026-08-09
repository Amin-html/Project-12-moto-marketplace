from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'price', 'quantity', 'subtotal']
        # subtotal — это @property, но DRF всё равно может его отдать
        # в fields, если он есть как атрибут на объекте модели


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'comment', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_price', 'shipping_address',
            'items', 'status_history', 'created_at',
        ]
        read_only_fields = ['status', 'total_price']
        # юзер не должен уметь сам менять статус или сумму заказа
        # через обычный PATCH запроса — только через отдельные вьюхи


class CreateOrderSerializer(serializers.Serializer):
    # serializers.Serializer, а не ModelSerializer — потому что
    # это не создаёт объект напрямую из полей, а принимает только
    # адрес, вся остальная логика (товары, сумма) идёт из корзины
    shipping_address = serializers.CharField(max_length=500)