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
    category = serializers.StringRelatedField()

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image', 'category')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для Продуктов"""
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'subcategory',
                  'price', 'image')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Корзины покупок"""
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'product', 'quantity')
