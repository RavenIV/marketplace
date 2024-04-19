from rest_framework import serializers

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
        read_only=True
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'product', 'amount', 'total_price')
        read_only_fields = ('id', 'product', 'total_price')
