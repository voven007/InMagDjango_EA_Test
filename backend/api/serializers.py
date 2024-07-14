from product.models import (
    Category, Product, ShoppingCart, SubCategory)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Категорий"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image')


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Подкатегорий"""

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image', 'category')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для Продуктов"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'subcategory',
                  'price', 'image')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Корзины покупок"""

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'product', 'quantity')
