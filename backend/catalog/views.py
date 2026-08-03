from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer
from core.permissions import IsSellerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsSellerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_type', 'category', 'brand']
    # фильтры вида /products/?product_type=motorcycle&brand=Honda

    search_fields = ['title', 'description', 'brand']
    # поиск вида /products/?search=honda

    ordering_fields = ['price', 'created_at']
    # сортировка вида /products/?ordering=-price (минус = по убыванию)

    def get_serializer_class(self):
        # разные сериалайзеры для чтения и записи
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        # подставляем текущего юзера как seller автоматически,
        # а не берём из тела запроса (see read_only_fields выше)
        serializer.save(seller=self.request.user)