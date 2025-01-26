from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет являться ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            # print(obj.owner.username)
            return True
        return False


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только владельцам объекта или суперпользователям.
    """

    def has_object_permission(self, request, view, obj):
        # Права на доступ чтения
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешите владельцу или суперпользователю
        return obj.owner == request.user or request.user.is_superuser
