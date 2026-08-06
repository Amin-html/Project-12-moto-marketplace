from django.db import models
from django.conf import settings
from catalog.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # тут total_price ХРАНИМ (не property!), потому что это заказ —
    # цены товаров могут потом измениться, а сумма заказа должна
    # остаться зафиксированной на момент покупки

    shipping_address = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # SET_NULL, а не CASCADE — если товар удалили из каталога,
    # заказ (историю покупки) это не должно стирать
    product_title = models.CharField(max_length=255)
    # дублируем название прямо тут — если товар потом удалят/переименуют,
    # в старом заказе останется то название, что было на момент покупки
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # и цену тоже дублируем — та же причина, "снимок" на момент заказа
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.Status.choices)
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # это и есть таймлайн со скрина: "23.07 Принята на складе",
    # "23.07 Готова к отправке", "25.07 Отправлена" — каждая запись
    # тут отдельная строка в этой таблице

    class Meta:
        ordering = ['created_at']