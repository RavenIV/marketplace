from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from PIL import Image

from .constants import MAX_CHAR_LENGTH, ICON_WIDTH, PREVIEW_WIDTH, MIN_PRODUCT_AMOUNT


class User(AbstractUser):
    pass


class CategoryBase(models.Model):
    """Базовый класс для категорий и подкатегорий."""
    title = models.CharField(
        'Название', max_length=MAX_CHAR_LENGTH, unique=True
    )
    slug = models.SlugField('Слаг', max_length=MAX_CHAR_LENGTH, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(CategoryBase):
    """Модель категорий."""
    image = models.ImageField(
        'Картинка',
        upload_to='images/categories/',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)


class Subcategory(CategoryBase):
    """Модель подкатегорий."""

    image = models.ImageField(
        'Картинка',
        upload_to='images/subcategories/',
    )
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
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1.00)]
    )
    subcategory = models.ForeignKey(
        to=Subcategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='products'
    )
    # shopped_by = models.ManyToManyField(
    #     to=User,
    #     blank=True,
    #     related_name='shopping_cart',
    #     verbose_name='Добавили в корзину'
    # )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'продукты'
        ordering = ('title',)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Модель изображений для продуктов."""
    class Size(models.TextChoices):
        ICON = 'ICON', 'Иконка'
        PREVIEW = 'PREVIEW', 'Превью'
        ORIGINAL = 'ORIGINAL', 'Оригинальный'

    size = models.CharField(
        'Размер',
        max_length=8,
        choices=Size.choices,
        default=Size.ORIGINAL,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image = models.ImageField(
        upload_to='images/products/',
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'изображения продукта'
        constraints = [
            UniqueConstraint(
                fields=('size', 'product'),
                name='unique_image_size'
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.size == ProductImage.Size.ICON:
            self.make_thumbnail(ICON_WIDTH)
        if self.size == ProductImage.Size.PREVIEW:
            self.make_thumbnail(PREVIEW_WIDTH)

    def make_thumbnail(self, target_width: int):
        image = Image.open(self.image)
        width, height = image.size
        height_coefficient = width/target_width
        target_height = int(height/height_coefficient)
        image.thumbnail((target_width, target_height))
        image.save(self.image.path)
        image.close()
        self.image.close()


class ShoppingCart(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='shopped_by',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(MIN_PRODUCT_AMOUNT)],
        default=MIN_PRODUCT_AMOUNT
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'корзины'
        constraints = [
            UniqueConstraint(
                fields=('product', 'user'),
                name='unique_product_in_cart'
            )
        ]

    @property
    def total_price(self):
        return self.product.price * self.amount
