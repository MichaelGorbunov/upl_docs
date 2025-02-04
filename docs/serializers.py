import hashlib
from datetime import datetime

from rest_framework.serializers import ModelSerializer

from docs.models import Upload

# from docs.services import send_message
from .validators import validate_file_size, validate_file_type


class DocsSerializer(ModelSerializer):
    """Сериализатор для документа"""

    # def update(self, instance):
    #     send_message()
    #     return instance
    class Meta:
        model = Upload
        fields = "__all__"
        read_only_fields = ["owner", "original_filename", "hash_file"]


class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"  # Указываем все поля модели
        read_only_fields = ["owner", "original_filename", "hash_file", "uploaded_at"]

    def validate_file(self, value):
        """Проверяем файл перед сохранением."""
        validate_file_type(value)  # Вызываем валидатор для типа файла
        validate_file_size(value)  # Вызываем валидатор для размера файла
        return value

    def create(self, validated_data):
        """Переопределяем метод create для добавления владельца и хэша файла."""
        uploaded_file = validated_data.pop("file")
        original_filename = uploaded_file.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_file = self.calculate_md5(uploaded_file)
        uploaded_file.name = f"{timestamp}_{uploaded_file.name}"

        # Создание экземпляра модели UploadedFile
        instance = Upload.objects.create(
            owner=self.context[
                "request"
            ].user,  # Устанавливаем владельца на текущего пользователя
            original_filename=original_filename,
            hash_file=hash_file,
            file=uploaded_file,
            **validated_data,
        )

        return instance

    def calculate_md5(self, file):
        """Вычисляет MD5-хэш для файла."""
        hash_md5 = hashlib.md5()
        for chunk in file.chunks():  # Используем метод chunks для считывания файла
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

# class UploadSerializer(ModelSerializer):
#     class Meta:
#         model = Upload
#         fields = "__all__"  # Укажите все нужные поля
#         read_only_fields = ["owner", "original_filename", "hash_file"]
#
#     def validate_file(self, value):
#         """Проверяем файл перед сохранением."""
#         validate_file_type(value)  # Вызываем валидатор для типа файла
#         validate_file_size(value)  # Вызываем валидатор для размера файла
#         return value
