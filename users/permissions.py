from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Убедимся, что `obj` — это пользователь, и он соответствует аутентифицированному пользователю.
        return obj == request.user