from django.core.validators import MinValueValidator
from rest_framework import serializers

from market.constants import MIN_PRODUCT_AMOUNT
from market.models import (
    Category, Subcategory, Product, ProductImage, ShoppingItem
)


class SubcategoryShortSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения подкатегорий."""

    class Meta:
        model = Subcategory
        fields = (
            'title',
            'slug',
            'image',
        )
        read_only_fields = fields


class CategoryShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'title',
            'slug',
            'image',
        )
        read_only_fields = fields


class CategoryDetailSerializer(CategoryShortSerializer):
    """Сериализатор для чтения категорий."""
    subcategories = SubcategoryShortSerializer(many=True, read_only=True)

    class Meta(CategoryShortSerializer.Meta):
        fields = (
            *CategoryShortSerializer.Meta.fields,
            'subcategories'
        )
        read_only_fields = fields


class ProductShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('slug', 'title', 'price')
        read_only_fields = fields


class SubcategoryDetailSerializer(SubcategoryShortSerializer):
    products = ProductShortSerializer(many=True, read_only=True)
    category = CategoryShortSerializer(read_only=True)

    class Meta(SubcategoryShortSerializer.Meta):
        fields = (
            *SubcategoryShortSerializer.Meta.fields,
            'category',
            'products'
        )
        read_only_fields = fields


class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('size', 'image')
        read_only_fields = fields


class ProductSerializer(ProductShortSerializer):
    subcategory = SubcategoryShortSerializer(read_only=True)
    category = CategoryShortSerializer(
        source='subcategory.category',
        read_only=True
    )
    images = ProductImagesSerializer(many=True, read_only=True)

    class Meta(ProductShortSerializer.Meta):
        fields = (
            *ProductShortSerializer.Meta.fields,
            'category',
            'subcategory',
            'images'
        )
        read_only_fields = fields


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    amount = serializers.IntegerField(
        validators=[MinValueValidator(MIN_PRODUCT_AMOUNT)]
    )

    class Meta:
        model = ShoppingItem
        fields = ('product', 'amount', 'total_price')
        read_only_fields = ('total_price',)
