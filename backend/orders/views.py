from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # юзер видит только свои заказы
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # transaction.atomic() — все операции внутри блока либо
            # выполнятся ВСЕ успешно, либо (если что-то упадёт на
            # середине) откатятся ВСЕ. Без этого можно получить
            # заказ без части товаров, если сервер упадёт посреди процесса
            order = Order.objects.create(
                user=request.user,
                total_price=cart.total_price,
                shipping_address=serializer.validated_data['shipping_address'],
            )

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_title=cart_item.product.title,
                    # "замораживаем" цену и название на момент покупки
                    price=cart_item.product.price,
                    quantity=cart_item.quantity,
                )

            OrderStatusHistory.objects.create(
                order=order, status=Order.Status.PENDING,
                comment='Order created',
            )

            cart.items.all().delete()
            # очищаем корзину после успешного оформления заказа

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_id):
        if request.user.role not in ['seller', 'admin']:
            return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        comment = request.data.get('comment', '')

        order.status = new_status
        order.save()

        OrderStatusHistory.objects.create(
            order=order, status=new_status, comment=comment,
        )
        # каждое обновление статуса — новая строка в истории,
        # это и создаёт таймлайн, который мы обсуждали

        return Response(OrderSerializer(order).data)