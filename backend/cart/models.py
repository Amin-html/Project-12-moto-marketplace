from django.db import models
from django.conf import settings
from catalog.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    # OneToOne — у каждого юзера ровно одна корзина (не создаём новую
    # при каждом добавлении товара, а переиспользуем одну и ту же)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    @property
    def total_price(self):
        # property — вычисляемое поле, не хранится в базе,
        # считается на лету при каждом обращении к cart.total_price
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        # unique_together — нельзя добавить один и тот же товар в корзину
        # дважды отдельными строками. Если юзер жмёт "добавить в корзину"
        # на товар, который уже там есть — увеличиваем quantity,
        # а не создаём вторую строку с тем же product

    @property
    def subtotal(self):
        return self.product.price * self.quantity