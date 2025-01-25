from rest_framework.serializers import ModelSerializer
from docs.models import Upload
# from docs.services import send_message
from .validators import validate_file_type
class DocsSerializer(ModelSerializer):
    """Сериализатор для документа"""

    # def update(self, instance):
    #     send_message()
    #     return instance
    class Meta:
        model = Upload
        fields = "__all__"

class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"  # Укажите все нужные поля

    def validate_file(self, value):
        """Проверяем файл перед сохранением."""
        validate_file_type(value)  # Вызываем наш валидатор
        return value