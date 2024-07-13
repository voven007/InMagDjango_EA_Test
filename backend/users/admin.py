from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',)
    search_fields = ('username', 'email')
    list_filter = ()
    list_display_links = ('username',)
    empty_value_display = 'Не задано'


admin.site.register(User, UserAdmin)
