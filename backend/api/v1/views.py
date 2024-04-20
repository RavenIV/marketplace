from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
)
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from market.models import Category, Product, Subcategory, ShoppingItem
from .serializers import (
    CategoryDetailSerializer,
    CategoryShortSerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    SubcategoryDetailSerializer,
    SubcategoryShortSerializer
)


class UserViewSet(DjoserViewSet):
    http_method_names = ['get', 'post']


class CategoryReadViewSet(ReadOnlyModelViewSet):
    """Получение списка категорий или конкретной категории."""
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryShortSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return Category.objects.prefetch_related('subcategories')
        return Category.objects.all()


class SubcategoryReadViewset(ReadOnlyModelViewSet):
    """Получение списка подкатегорий или конкретной категории."""
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubcategoryDetailSerializer
        return SubcategoryShortSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return Subcategory.objects.prefetch_related('products', 'category')
        return Subcategory.objects.all()


class ProductReadViewSet(ReadOnlyModelViewSet):
    """Получение списка продуктов или конкретного продукта."""
    queryset = Product.objects.prefetch_related(
        'subcategory', 'subcategory__category', 'images'
    )
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ShoppingView(APIView):
    """
    Добавление, изменение количества или удаление
    продукта из корзины пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get_product(self, product_slug):
        return get_object_or_404(
            Product,
            slug=product_slug
        )

    def get_shopping_item(self, product):
        return get_object_or_404(
            ShoppingItem,
            user=self.request.user,
            product=product
        )

    @extend_schema(responses={201: ShoppingCartSerializer})
    def post(self, request, product_slug):
        """Добавить продукт в корзину."""
        product = self.get_product(product_slug)
        user = self.request.user
        if ShoppingItem.objects.filter(
            product=product,
            user=user
        ).exists():
            raise ValidationError('Продукт уже есть в корзине')
        shopping_item = ShoppingItem.objects.create(
            product=product,
            user=user
        )
        serializer_data = ShoppingCartSerializer(shopping_item).data
        return Response(serializer_data, status=HTTP_201_CREATED)

    @extend_schema(
        request=ShoppingCartSerializer,
        responses={200: ShoppingCartSerializer}
    )
    def patch(self, request, product_slug):
        """Изменить количество продукта в корзине."""
        product = self.get_product(product_slug)
        shopping_item = self.get_shopping_item(product)
        serializer = ShoppingCartSerializer(
            shopping_item, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, product_slug):
        """Удалить продукт из корзины."""
        product = self.get_product(product_slug)
        shopping_item = self.get_shopping_item(product)
        shopping_item.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ShoppingCartView(APIView):
    """Просмотр корзины пользователя или ее удаление."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShoppingItem.objects.filter(
            user=self.request.user
        )

    def get(self, request):
        """Вевести состав корзины покупок."""
        results = self.get_queryset().aggregate(
            total_sum=Sum(F('product__price') * F('amount')),
            positions_count=Count('product')
        )
        shopping_items_data = ShoppingCartSerializer(
            self.get_queryset(), many=True
        ).data
        return Response(
            data=dict(**results, products=shopping_items_data),
            status=HTTP_200_OK
        )

    def delete(self, request):
        """Очистить корзину покупок."""
        shopping_cart = self.get_queryset()
        if not shopping_cart:
            raise ValidationError('В корзине нет товаров.')
        shopping_cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)
