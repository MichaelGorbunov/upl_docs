from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from docs.models import Upload
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

    def test_5file_upload(self):
        """Тест загрузки файла"""

        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        # Создайте временный файл
        file_content = b"This is a test file."
        uploaded_file = SimpleUploadedFile("testfile.txt", file_content)

        # Отправьте POST-запрос к вашему API с файлом
        response = self.client.post("/docs/create/", {"file": uploaded_file})

        # Проверьте статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
