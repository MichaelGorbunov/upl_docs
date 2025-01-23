# from django.shortcuts import render
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,DestroyAPIView
                                     )

from docs.models import Upload
from docs.serializers import DocsSerializer
from docs.services import print_message


class DocsListAPIView(ListAPIView):
    """Контроллер вывода списка документов"""

    queryset = Upload.objects.all()
    serializer_class = DocsSerializer



class DocsCreateAPIView(CreateAPIView):
    """Контроллер создания нового документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()

    def perform_create(self, serializer):
        """Автоматическая запись пользователя в атрибут owner """
        docs = serializer.save()
        docs.owner = self.request.user
        print_message()
        docs.save()


class DocsDestroyAPIView(DestroyAPIView):
    """Контроллер удаления одного документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()
    # permission_classes = (IsOwner,)
