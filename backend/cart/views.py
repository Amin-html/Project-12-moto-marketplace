from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer
from catalog.models import Product

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # get_or_create — вернёт существующую корзину юзера,
        # а если её ещё нет (первый визит) — создаст пустую
        cart, _ = Cart.objects.get_or
        _create(user=self.request.user)
        return cart


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity},
        )
        if not created:
            # товар уже был в корзине — просто увеличиваем количество,
            # а не создаём вторую строку (это и защищает unique_together)
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
        # cart__user=request.user — двойная защита: удалить можно
        # только свой item, а не чужой по угаданному ID
        return Response(status=status.HTTP_204_NO_CONTENT)