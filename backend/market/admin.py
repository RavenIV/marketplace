from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Product,
    ProductImage,
    Subcategory,
    User
)


class ProductImagesInline(admin.StackedInline):
    model = ProductImage
    max_num = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'image_tag',
    )
    search_fields = ('title', 'slug')

    @admin.display(description='Картинка')
    @mark_safe
    def image_tag(self, category):
        return '<img src="{}" width="75px" height="75" />'.format(
            category.image.url
        )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'image_tag',
    )
    search_fields = ('title', 'slug')
    list_filter = ['category__title']

    @admin.display(description='Картинка')
    @mark_safe
    def image_tag(self, subcategory):
        return '<img src="{}" width="75px" height="75px" />'.format(
            subcategory.image.url
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
    list_display = (
        'title',
        'slug',
        'price',
    )
    list_filter = ['subcategory__title']


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.site_header = 'Портал администратора Marketplace'
admin.site.site_title = 'Портал администратора'
admin.site.index_title = (
    'Добро пожаловать на портал администратора Marketplace!'
)
