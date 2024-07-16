"""
Набор подключаемых разрешений.
"""
from rest_framework import permissions


class Author(permissions.BasePermission):
    """Редактирование/удаление объекта доступно только автору объекта."""
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)
