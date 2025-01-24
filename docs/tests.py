from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from docs.models import Upload
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser



class FileUploadTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="user1@habits.ru", username="user1", password="12345678")
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
    def test_file_upload(self):
        '''Тест загрузки файла'''
        # Создайте временный файл
        file_content = b'This is a test file.'
        uploaded_file = SimpleUploadedFile("testfile.txt", file_content)

        # Отправьте POST-запрос к вашему API с файлом
        response = self.client.post('/docs/create/', {'file': uploaded_file})

        # Проверьте статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
