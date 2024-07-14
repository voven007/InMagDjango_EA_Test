from api.serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer,
    ShoppingCartSerializer
)
from product.models import (
    Category, Product, ShoppingCart, SubCategory)
from rest_framework import viewsets
from rest_framework.permissions import (
    SAFE_METHODS, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from users.models import User


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Подкатегорий"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (AllowAny,)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ShoppingCartViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Корзины покупок"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (AllowAny,)
