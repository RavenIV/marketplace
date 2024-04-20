from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView

from market.models import Category, Product, ShoppingCart
from .serializers import CategorySerializer, ProductSerializer, ShoppingCartSerializer


class UserViewSet(DjoserViewSet):
    http_method_names = ['get', 'post']


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


class ShoppingCartView(APIView):


    # def get_product(self, product_slug):
    #     return get_object_or_404(
    #         Product,
    #         slug=product_slug
    #     )

    # def get_object(self):
    #     return get_object_or_404(
    #         ShoppingCart,
    #         user=self.request.user,
    #         product=self.get_product()
    #     )

    @extend_schema(
        request=ShoppingCartSerializer,
        responses={201: ShoppingCartSerializer}
    )
    def post(self, request, product_slug):
        """Добавить продукт в корзину."""
        request.data['product'] = product_slug
        serializer = ShoppingCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    