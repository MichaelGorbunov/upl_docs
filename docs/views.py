# from django.shortcuts import render
from rest_framework.generics import (CreateAPIView,
                                     ListAPIView,DestroyAPIView
                                     )

from docs.models import Upload
from docs.serializers import DocsSerializer
from docs.services import send_message
from docs.permissions import IsOwner,IsOwnerOrSuperUser

from rest_framework.permissions import IsAuthenticated



class DocsListAPIView(ListAPIView):
    """Контроллер вывода списка документов"""

    # queryset = Upload.objects.all()
    serializer_class = DocsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получите пользователя из запроса
        user = self.request.user

        # Если пользователь суперпользователь, возвращаем все документы
        if user.is_superuser:
            return Upload.objects.all()

        # В противном случае, возвращаем только документы владельца
        return Upload.objects.filter(owner=user)


class DocsCreateAPIView(CreateAPIView):
    """Контроллер создания нового документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()

    def perform_create(self, serializer):
        """Автоматическая запись пользователя в атрибут owner """
        docs = serializer.save()
        docs.owner = self.request.user
        send_message(f"Загружен новый документ {docs.file} ")
        docs.save()


class DocsDestroyAPIView(DestroyAPIView):
    """Контроллер удаления одного документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()
    # permission_classes = [IsAuthenticated,]
    permission_classes = [IsOwner]
