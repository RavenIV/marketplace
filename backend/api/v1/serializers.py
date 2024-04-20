from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from market.models import (
    Category, Subcategory, Product, ProductImage, ShoppingCart
)


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для чтения подкатегорий."""

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'title',
            'slug',
            'image',
        )
        read_only_fields = fields


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для чтения категорий."""
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'image',
            'subcategories'
        )
        read_only_fields = fields


class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('size', 'image')
        read_only_fields = fields


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        slug_field='title', read_only=True
    )
    category = serializers.SlugRelatedField(
        slug_field='title',
        source='subcategory.category',
        read_only=True
    )
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'category',
            'subcategory',
            'price',
            'images'
        )
        read_only_fields = fields


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Product.objects.all()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'product', 'user', 'amount', 'total_price')
        read_only_fields = ('id', 'total_price')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('product', 'user')
            )
        ]
