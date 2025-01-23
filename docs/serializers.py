from rest_framework.serializers import ModelSerializer
from docs.models import Upload
# from docs.services import send_message

class DocsSerializer(ModelSerializer):
    """Сериализатор для документа"""

    # def update(self, instance):
    #     send_message()
    #     return instance
    class Meta:
        model = Upload
        fields = "__all__"
