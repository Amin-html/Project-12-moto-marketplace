from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children',
    )
    # 'self' — ForeignKey на саму себя. Нужно для вложенных категорий:
    # "Запчасти" -> "Двигатель" -> "Поршни". parent=None значит
    # это категория верхнего уровня.

    def __str__(self):
        return self.name


class Product(models.Model):
    class ProductType(models.TextChoices):
        MOTORCYCLE = 'motorcycle', 'Motorcycle'
        PART = 'part', 'Part'
        TUNING = 'tuning', 'Tuning'

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
    )
    # ForeignKey на User (не SellerProfile напрямую) — так проще:
    # у одного User может быть много Product, а сам User уже
    # содержит role и, при необходимости, related seller_profile.

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='products',
    )
    # SET_NULL, а не CASCADE — если удалили категорию,
    # товары не должны исчезать, просто останутся без категории.
    # Поэтому category тоже обязан быть null=True.

    product_type = models.CharField(max_length=20, choices=ProductType.choices)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # DecimalField, а не FloatField — для денег ВСЕГДА Decimal,
    # у float есть погрешности округления (0.1 + 0.2 != 0.3 в float)

    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)

    # Специфичные поля - опциональные, для не-мотоциклов просто пустые
    year = models.PositiveIntegerField(null=True, blank=True)
    engine_volume = models.PositiveIntegerField(null=True, blank=True)  # см³
    compatible_models = models.CharField(max_length=255, blank=True)   # для запчастей

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images',
    )
    image = models.ImageField(upload_to='products/images/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    # order - для сортировки, какое фото показывать первым в галерее

    def __str__(self):
        return f'{self.product.title} - image {self.id}'


class ProductVideo(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='videos',
    )
    video = models.FileField(upload_to='products/videos/')

    def __str__(self):
        return f'{self.product.title} - video {self.id}'