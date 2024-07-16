from product.models import (
    CartProduct, Category, Product, ShoppingCart, SubCategory)
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
    images = serializers.ListSerializer(
        child=serializers.ImageField(), read_only=True
    )
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'subcategory',
                  'price', 'image', 'images')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Корзины покупок"""
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    id = serializers.IntegerField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'product')

    def validate_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f'{value} - продукта не существует.'
            )
        return value


class AmountProductSerializer(serializers.ModelSerializer):
    """Поле продукт/кол-во/стоимость при Get запросе к корзине."""
    id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')
    purchase = serializers.IntegerField()

    class Meta:
        model = CartProduct
        fields = (
            'id', 'name', 'price', 'amount', 'purchase'
        )


class GetShoppingCartSerializer(serializers.ModelSerializer):
    """Корзина."""
    products = AmountProductSerializer(
        many=True, source='cart_products'
    )
    count_product = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('id', 'products', 'count_product')
        depth = 1

    def get_count_product(self, obj):
        obj.cart_products.count()
        return obj.cart_products.count()


class CreateUpdateShoppingCartSerializer(serializers.ModelSerializer):
    """Создание/редактирование корзины."""
    products = ShoppingCartSerializer(many=True)

    class Meta:
        model = ShoppingCart
        depth = 1
        exclude = ('user',)
        read_only_fields = ('user',)

    def validate(self, data):
        if (
            self.context['request'].method in ['POST']
            and ShoppingCart.objects.filter(user=self.context['request'].user).exists()
        ):
            raise serializers.ValidationError('Корзина уже существует.')
        products_data = data.get('products')
        if not products_data:
            raise serializers.ValidationError('Необходимо ввести продукт.')
        products = [index['id'] for index in products_data]
        if len(products) != len(set(products)):
            raise serializers.ValidationError(
                'Продукты не могут повторяться!'
            )
        return data

    def save_products(self, products, cart):
        CartProduct.objects.bulk_create(
            [CartProduct(
                product=Product.objects.get(id=product['id']),
                cart=cart,
                amount=product.get('amount')
            ) for product in products]
        )

    def create(self, validated_data):
        products = validated_data.pop('products')
        cart = ShoppingCart.objects.create(**validated_data)
        self.save_products(
            products=products,
            cart=cart
        )
        return cart

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        instance = super().update(instance, validated_data)
        instance.products.clear()
        self.save_products(
            products=products,
            cart=instance
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return GetShoppingCartSerializer(instance, context=context).data


class DeleteProductShoppingCartSerializer(serializers.Serializer):
    """Удаление товара из таблицы CartProduct."""
    id_product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )


class ProductShoppingCartSerializer(DeleteProductShoppingCartSerializer):
    """Добавление товара в таблицу CartProduct."""
    amount = serializers.IntegerField()
