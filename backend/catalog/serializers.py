from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVideo

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'order']


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['id', 'video']


class ProductSerializer(serializers.ModelSerializer):
    # nested-сериалайзеры — вложенные объекты вместо просто ID.
    # Так в JSON-ответе на /products/1/ фото придут не как [1, 2, 3],
    # а сразу полными объектами с ссылками на файлы.
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)

    # read_only-поля для удобного отображения (а не только ID продавца/категории)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_username', 'category', 'category_name',
            'product_type', 'title', 'slug', 'description', 'price',
            'stock', 'brand', 'year', 'engine_volume', 'compatible_models',
            'is_active', 'images', 'videos', 'created_at',
        ]
        read_only_fields = ['seller']
        # seller read_only — юзер не должен сам вписывать чужой ID продавца
        # в теле запроса, мы подставим request.user на бэке (см. views.py)


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Отдельный сериалайзер для создания — без вложенных read_only полей,
    чтобы не путать вход и выход. При создании фото/видео загружаются
    отдельным запросом после создания товара (проще для API).
    """
    class Meta:
        model = Product
        fields = [
            'category', 'product_type', 'title', 'slug', 'description',
            'price', 'stock', 'brand', 'year', 'engine_volume',
            'compatible_models',
        ]