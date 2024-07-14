from django.core.validators import RegexValidator
from django.db import models
from users.models import User
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit


class BaseCategoryModel(models.Model):
    """Базовая модель категорий"""
    name = models.CharField(
        verbose_name='Название',
        max_length=128
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=32,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ в Слаге'
        )]
    )
    image = ProcessedImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/category',
        processors=[ResizeToFit(380, 380)],
        format='JPEG', options={'quality': 70}
    )

    class Meta:
        abstract = True
        ordering = ('id',)


class Category(BaseCategoryModel):
    """Модель категории товара"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(BaseCategoryModel):
    """Модель подкатегории товара"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='sub_category_list',
        verbose_name='Подкатегория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(
        verbose_name='Название продукта',
        db_index=True,
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=32,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Недопустимый символ в Слаге'
        )]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='product_category',
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='product_sub_category',
        verbose_name='Подкатегория'
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images'
    )
    image_midi = ImageSpecField(
        processors=[ResizeToFit(150, 150)],
        format='JPEG',
        options={'quality': 60}
    )
    image_mini = ImageSpecField(
        processors=[ResizeToFit(60, 60)],
        format='JPEG',
        options={'quality': 60}
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    @property
    def images(self):
        return [self.image, self.image_midi, self.image_mini]


class ImageResisez(models.Model):
    """Модель трех изображений"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    image_1 = models.ImageField(
        verbose_name='Изображение_1',
        upload_to='recipes/images/resisez'
    )
    image_2 = models.ImageField(
        verbose_name='Изображение_2',
        upload_to='recipes/images/resisez'
    )
    image_3 = models.ImageField(
        verbose_name='Изображение_3',
        upload_to='recipes/images/resisez'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.product


class ShoppingCart(models.Model):
    """Модель списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('product',)
        default_related_name = 'product_shopping'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.user} добавил "{self.product}" в свою корзину'
