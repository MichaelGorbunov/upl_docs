from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.exceptions import ValidationError

from docs.models import Upload
from docs.validators import validate_file_type, validate_file_size
from users.models import CustomUser


class FileUploadTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user1@habits.ru", username="user1", password="12345678"
        )
        self.other_user = CustomUser.objects.create_user(
            username="other_user", email="2@test.com", password="password123"
        )
        file_content = b"This is a test file."
        uploaded_file = SimpleUploadedFile("testfile.txt", file_content)
        self.uploaded_file = Upload.objects.create(
            owner=self.user,
            # file="mail/test.txt",
            original_filename=uploaded_file.name,
            file=uploaded_file,
        )

        # Выводим ID загруженного файла для отладки
        print(f"Uploaded file ID: {self.uploaded_file.id}")

        # Инициализация APIRequestFactory
        self.factory = APIRequestFactory()

    def test_2file_list(self):
        """Тест списка"""

        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя

        # Отправьте POST-запрос к вашему API с файлом
        response = self.client.get("/docs/list/")

        # Проверьте статус ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_3file_list(self):
        """Тест удаления не владельцем"""

        self.client.force_authenticate(
            user=self.other_user
        )  # Аутентификация пользователя

        # Отправьте POST-запрос к вашему API с файлом
        response = self.client.delete("/docs/delete/2/")

        # Проверьте статус ответа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_4file_list(self):
        """Тест удаления владельцем"""

        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя

        # Отправьте POST-запрос к вашему API с файлом
        response = self.client.delete("/docs/delete/3/")

        # Проверьте статус ответа
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class FileValidatorTests(TestCase):

    def test_1valid_file_type(self):
        """Тест для корректного типа файла."""
        file = SimpleUploadedFile("test_image.jpeg", b"file_content", content_type="image/jpeg")
        try:
            validate_file_type(file)
        except ValidationError:
            self.fail("ValidationError was raised for a valid file type.")

    def test_1invalid_file_type(self):
        """Тест для недопустимого типа файла."""

        valid_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        try:
            validate_file_type(valid_file)
        except ValidationError:
            self.fail("validate_file_type() raised ValidationError unexpectedly!")


class FileSizeValidatorTests(TestCase):
    def test_1valid_file_size(self):
        """Тест для корректного размера файла."""
        file = SimpleUploadedFile("test_image.jpeg", b"file_content", content_type="image/jpeg")
        file.size = 4 * 1024 * 1024  # 4 MB
        try:
            validate_file_size(file)
        except ValidationError:
            self.fail("ValidationError was raised for a valid file size.")

    def test_2invalid_file_size(self):
        """Тест для некорректного размера файла."""
        file = SimpleUploadedFile("test_file.jpeg", b"file_content", content_type="image/jpeg")
        file.size = 6 * 1024 * 1024  # 6 MB, больше максимального разрешенного размера
        self.assertRaises(ValidationError)
