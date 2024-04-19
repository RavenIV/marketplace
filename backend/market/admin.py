from django.contrib import admin

from .models import Category, Subcategory, Product, ProductImage


class ProductImagesInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product, ProductAdmin)
