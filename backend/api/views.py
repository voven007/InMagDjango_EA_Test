
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from product.models import CartProduct, Category, Product, SubCategory
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from api.permissions import Author
from api.serializers import (AmountProductSerializer, CategorySerializer,
                             CreateUpdateShoppingCartSerializer,
                             DeleteProductShoppingCartSerializer,
                             GetShoppingCartSerializer, ProductSerializer,
                             ProductShoppingCartSerializer,
                             SubCategorySerializer)

from .paginators import PageLimitPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPagination


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Подкатегорий"""
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageLimitPagination


class ShoppingCartViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Корзины покупок"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'create')

    def get_serializer_class(self):
        if self.action in ('list',):
            return GetShoppingCartSerializer
        return CreateUpdateShoppingCartSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.users.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(request_body=ProductShoppingCartSerializer,
                         responses={201: AmountProductSerializer})
    @action(
        permission_classes=(Author,),
        methods=('post',), detail=True
    )
    def product_cart(self, request, pk=None):
        """Добавляем продукт в корзину."""
        cart = self.get_object()
        product = get_object_or_404(Product, id=request.data.get('id_product'))
        amount = request.data.get('amount')
        if amount < 1:
            return Response(
                {'errors': 'Количество не может быть меньше 1.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart, product=product
        )
        cart_product.amount = amount
        cart_product.save(update_fields=['amount'])
        return Response(
            AmountProductSerializer(cart_product).data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(request_body=DeleteProductShoppingCartSerializer,
                         responses={204: 'Товар удален из корзины'})
    @product_cart.mapping.delete
    def delete_product_cart(self, request, pk=None):
        """Удаляем продукт из корзины."""
        cart = self.get_object()
        cart.cart_products.filter(
            product=request.data.get('id_product')
        ).delete()
        return Response('Товар удален из корзины',
                        status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={204: 'Все товары удалены из корзины'})
    @action(
        permission_classes=(Author,),
        methods=('delete',), detail=True
    )
    def clean_all(self, request, pk=None):
        """Полная очистка корзины."""
        cart = self.get_object()
        self.perform_destroy(
            cart.cart_products.all()
        )
        return Response('Все товары удалены из корзины',
                        status=status.HTTP_204_NO_CONTENT)
