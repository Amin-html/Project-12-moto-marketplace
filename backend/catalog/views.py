from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer
from core.permissions import IsSellerOrReadOnly
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsSellerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_type', 'category', 'brand']
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        cache.delete_pattern('products_list_*')
        # при создании нового товара — стираем закэшированные списки,
        # иначе новый товар не появится в выдаче пока кэш не протухнет сам

    def perform_update(self, serializer):
        serializer.save()
        cache.delete_pattern('products_list_*')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete_pattern('products_list_*')

    def list(self, request, *args, **kwargs):
        # свой кэш-ключ учитывает query-параметры (фильтры/поиск/сортировку),
        # иначе разные фильтрованные списки будут путаться в одном кэше
        cache_key = f'products_list_{request.GET.urlencode()}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        # timeout=300 секунд (5 минут) — на случай если что-то пойдёт
        # не так с delete_pattern, кэш всё равно сам протухнет
        return response