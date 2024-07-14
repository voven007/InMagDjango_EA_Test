from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, SubCategoryViewSet, ProductViewSet, ShoppingCartViewSet
)

app_name = 'api'
router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('subcategory', SubCategoryViewSet, basename='subcategory')
router.register('product', ProductViewSet, basename='product')
router.register('shoppingcart', ShoppingCartViewSet, basename='shoppingcart')

urlpatterns = [
    path('', include(router.urls)),
]
