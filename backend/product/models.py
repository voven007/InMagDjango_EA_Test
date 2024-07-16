from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit
from users.models import User


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

    def __str__(self):
        return '{name} {slug}'.format(
            name=self.name,
            slug=self.slug
        )


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
        return '{subcategory}'.format(
            subcategory=self.name
        )


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
        return '{subcategory} {price}'.format(
            subcategory=self.subcategory.name,
            price=self.price
        ) + super().__str__()

    @property
    def images(self):
        return [self.image, self.image_midi, self.image_mini]


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

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return '{user}, {product}'.format(
            user=self.user.username,
            product=self.product
        )


class CartProduct(models.Model):
    """Модель связи корзины пользователя и товара"""
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='products'
    )
    cart = models.ForeignKey(
        ShoppingCart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    amount = models.IntegerField(
        verbose_name='Кол-во',
        default=1,
        validators=(MinValueValidator(1),)
    )

    class Meta:
        ordering = ('cart',)
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_cartproduct'
            )
        ]

    def __str__(self):
        return '{cart}, {product}, {amount}'.format(
            cart=self.cart,
            product=self.product.name,
            amount=self.amount
        )

    @property
    def purchase(self):
        return self.product.price * self.amount
