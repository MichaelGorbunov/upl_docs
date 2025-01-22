from rest_framework.test import APITestCase
# from rest_framework.permissions import BasePermission
# from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .permissions import IsAccountOwner
from .models import CustomUser


# from .serializer import CustomUserDetailSerializer, CustomUserSerializer
# from .views import CustomUserViewSet


class IsAccountOwnerTestCase(APITestCase):
    def setUp(self):
        # Создание двух пользователей
        self.owner_user = CustomUser.objects.create_user(
            email="owner@habits.ru", password="123456789", username="ownerUser"
        )
        self.other_user = CustomUser.objects.create_user(
            email="other@habits.ru", password="987654321", username="otherUser"
        )

        # Инициализация APIRequestFactory для mock-запросов
        self.factory = APIRequestFactory()
        self.permission = IsAccountOwner()

    def test_permission_owner_access(self):
        """
        Проверяем, что пользователь может получить доступ к собственному объекту.
        """
        # Создаём mock-запрос от имени владельца
        request = self.factory.get("/mock-url/")
        request.user = self.owner_user

        # permission: has_object_permission(request, view, obj)
        is_permitted = self.permission.has_object_permission(
            request, None, self.owner_user
        )

        self.assertTrue(is_permitted, "Владелец объекта должен иметь доступ.")

    def test_permission_other_user_access(self):
        """
        Проверяем, что другой пользователь НЕ имеет доступа к объекту.
        """
        # Создаём mock-запрос от имени другого пользователя
        request = self.factory.get("/mock-url/")
        request.user = self.other_user

        # Проверяем разрешение на доступ
        is_permitted = self.permission.has_object_permission(
            request, None, self.owner_user
        )

        self.assertFalse(is_permitted, "Другой пользователь не должен иметь доступ.")

    def test_permission_unauthenticated_access(self):
        """
        Проверяем, что неаутентифицированный пользователь НЕ имеет доступа.
        """
        # Создаём mock-запрос без авторизации
        request = self.factory.get("/mock-url/")
        request.user = None

        # Проверяем разрешение на доступ
        is_permitted = self.permission.has_object_permission(
            request, None, self.owner_user
        )

        self.assertFalse(is_permitted, "Неаутентифицированный пользователь не должен иметь доступ.")
