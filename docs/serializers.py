from rest_framework.serializers import ModelSerializer
from docs.models import Upload


class DocsSerializer(ModelSerializer):
    """Сериализатор для привычки"""

    class Meta:
        model = Upload
        fields = "__all__"
