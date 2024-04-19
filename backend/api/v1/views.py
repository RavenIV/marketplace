from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from market.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(ListAPIView):
    """Получение списка категорий."""
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """Получение списка продуктов или конкретного продукта."""
    queryset = Product.objects.prefetch_related(
        'subcategory', 'images'
    )
    serializer_class = ProductSerializer
    lookup_field = 'slug'
