from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import MAX_CHAR_LENGTH


class User(AbstractUser):
    pass


class CategoryBase(models.Model):
    """Базовый класс для категорий и подкатегорий."""
    title = models.CharField(
        'Название', max_length=MAX_CHAR_LENGTH, unique=True
    )
    slug = models.SlugField('Слаг', max_length=MAX_CHAR_LENGTH, unique=True)
    image = models.ImageField('Картинка', upload_to='market/images')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(CategoryBase):
    """Модель категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)


class Subcategory(CategoryBase):
    """Модель подкатегорий."""

    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='subcategories',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'подкатегории'
        ordering = ('title',)


class Product(models.Model):
    title = models.CharField('Название', max_length=MAX_CHAR_LENGTH)
    slug = models.SlugField('Слаг', max_length=MAX_CHAR_LENGTH, unique=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    subcategory = models.ForeignKey(
        to=Subcategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='products'
    )
    shopped_by = models.ManyToManyField(
        to=User,
        blank=True,
        related_name='shopping_cart',
        verbose_name='Добавили в корзину'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'продукты'
        ordering = ('title',)
