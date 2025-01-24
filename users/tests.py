from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
# from rest_framework.permissions import BasePermission
# from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
import pytest
from .permissions import IsAccountOwner
from .models import CustomUser
from django.urls import reverse

# from .serializer import CustomUserDetailSerializer, CustomUserSerializer
# from .views import CustomUserViewSet

from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User
from io import StringIO

from .serializer import CustomUserDetailSerializer, CustomUserSerializer
from .views import CustomUserViewSet


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


class CreateUserCommandTest(TestCase):
    '''тестирование кастомной команды'''

    def test_create_user_command(self):
        '''проверка создания пользователя'''
        # Перенаправляем вывод команды в строковый буфер

        call_command('csu')

        # Проверяем, что пользователь был создан
        user = CustomUser.objects.filter(username='SuperUser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('123456789'))  # Проверяем правильность пароля


class CustomUserViewSetTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """Создает тестового пользователя для проведения тестов."""
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        cls.client = APITestCase()  # Создание экземпляра клиента

    def test_authenticated_user_can_retrieve_user(self):
        """Тест: аутентифицированный пользователь может получить данные конкретного пользователя."""
        url = f"/users/users/{self.user.id}/"
        # url = ('users-detail', args=[self.user.id])
        self.client.force_authenticate(user=self.user)  # Имитация аутентифицированного пользователя

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_unauthenticated_user_cannot_retrieve_user(self):
        """Тест: неаутентифицированный пользователь не может получить данные пользователя."""
        url = f"/users/users/{self.user.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_update_user(self):
        """Тест: аутентифицированный пользователь может обновить свои данные."""
        url = f"/users/users/{self.user.id}/"
        self.client.force_authenticate(user=self.user)

        updated_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newpassword'
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что данные обновлены
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_authenticated_user_can_delete_user(self):
        """Тест: аутентифицированный пользователь может удалить свою учетную запись."""
        url = f"/users/users/{self.user.id}/"
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.user.id).exists())
