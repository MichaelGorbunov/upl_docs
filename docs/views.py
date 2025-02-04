# from django.shortcuts import render
# import hashlib
# import os
# from datetime import datetime

# from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.models import Upload
from docs.permissions import IsOwner, IsOwnerOrSuperUser
from docs.serializers import DocsSerializer, UploadSerializer
# from docs.services import send_message
from docs.tasks import send_email_to_admin


class DocsListAPIView(ListAPIView):
    """Контроллер вывода списка документов"""

    # queryset = Upload.objects.all()
    serializer_class = DocsSerializer
    permission_classes = [IsOwnerOrSuperUser]

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

    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "В запросе нет файла"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            send_email_to_admin.delay(f"Загружен файл {instance.original_filename}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocsDestroyAPIView(DestroyAPIView):
    """Контроллер удаления одного документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()
    # permission_classes = [IsAuthenticated,]
    permission_classes = [IsOwner]


class FileDownloadView(APIView):
    """Контроллер скачивания документа"""

    permission_classes = [IsOwnerOrSuperUser]

    # serializer_class = DocsSerializer
    # queryset = Upload.objects.all()
    def get_queryset(self):
        # Получите пользователя из запроса
        user = self.request.user

        # Если пользователь суперпользователь, возвращаем все документы
        if user.is_superuser:
            return Upload.objects.all()

        # В противном случае, возвращаем только документы владельца
        return Upload.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        try:
            # Получаем объект файла
            file_instance = Upload.objects.get(pk=kwargs["pk"])
        except Upload.DoesNotExist:
            raise Http404("File not found")

        # Используем оригинальное имя файла для скачивания
        original_filename = file_instance.original_filename or file_instance.file.name

        # Создаем ответ для скачивания файла
        response = HttpResponse(
            file_instance.file, content_type="application/octet-stream"
        )
        # response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
        response["Content-Disposition"] = f'attachment; filename="{original_filename}"'
        return response
