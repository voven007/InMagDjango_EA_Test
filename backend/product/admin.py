from django.contrib import admin

from .models import Category, Product, ShoppingCart, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'image',)
    list_editable = ()
    search_fields = ('name',)
    list_filter = ()
    list_display_links = ('name',)
    empty_value_display = 'Не задано'


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'category',
        'image',)
    list_editable = ()
    search_fields = ('name',)
    list_filter = ()
    list_display_links = ('name',)
    empty_value_display = 'Не задано'


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'category',
        'subcategory',
        'price',
        'image',
        'image_midi',
        'image_mini',)
    list_editable = ()
    search_fields = ('name',)
    list_filter = ('category', 'subcategory',)
    list_display_links = ('name',)
    empty_value_display = 'Не задано'

    # @admin.display(description="Добавлено в избранное")
    # def number_to_favorites(self, obj):
    #     return Favorite.objects.filter(recipe=obj).count()


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product')
    list_editable = ()
    search_fields = ('user',)
    list_filter = ()
    list_display_links = ('user',)
    empty_value_display = 'Не задано'


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
