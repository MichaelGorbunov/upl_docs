# from django.shortcuts import render
import hashlib
import os
from datetime import datetime

from django.core.files.base import ContentFile
from django.http import Http404, HttpResponse
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
)
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

    serializer_class = UploadSerializer
    queryset = Upload.objects.all()
    permission_classes = [IsAuthenticated]
# тоже не работает
    # def perform_create(self, serializer):
    #     # Получаем загруженный файл
    #     uploaded_file = self.request.FILES['uploaded_file']
    #
    #     # Сохраняем оригинальное имя файла
    #     original_file_name = uploaded_file.name
    #
    #     # Добавляем дату и время к имени файла
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     _, ext = os.path.splitext(uploaded_file.name)
    #     new_file_name = f"{timestamp}{ext}"
    #     # new_file_name = f"{self.request.data['title']}_{timestamp}{ext}"
    #
    #     # Вычисляем MD5 хеш
    #     hash_file = self.calculate_md5(uploaded_file)
    #
    #     # Создаем экземпляр модели
    #     serializer.save(
    #         owner=self.request.user,
    #         original_file_name=original_file_name,
    #         file=new_file_name,
    #         hash_file=hash_file
    #     )
# пустые файлы
    def post(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "В запросе нет файла"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]
            original_filename = uploaded_file.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            hash_file = self.calculate_md5(uploaded_file)

            # Измените имя файла, добавив временную метку
            new_file_name = f"{timestamp}_{uploaded_file.name}"
            new_file = ContentFile(uploaded_file.read(), name=new_file_name)
            uploaded_file.name = f"{timestamp}_{uploaded_file.name}"

            # Создание экземпляра модели UploadedFile
            uploaded_instance = Upload(
                owner=request.user,  # Устанавливаем владельца на текущего пользователя
                # original_filename=uploaded_file.name,
                original_filename=original_filename,
                # name=new_file_name,
                hash_file=hash_file,
                # file=new_file,  # файл будет сохранен автоматически
                file=uploaded_file

            )
            uploaded_instance.save()
            # телеграмм
            # send_message(f"Загружен новый документ {original_filename} ")
            send_email_to_admin.delay(f"Загружен файл {original_filename} ")

            return Response(
                {"original_name": original_filename, "new_name": uploaded_file.name},
                status=status.HTTP_201_CREATED,
            )
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def calculate_md5(self, file):
        """Вычисляет MD5-хэш для файла."""
        hash_md5 = hashlib.md5()
        # Считываем файл по частям
        for chunk in file.chunks():  # Используем метод chunks для считывания файла
            hash_md5.update(chunk)

        return hash_md5.hexdigest()


class DocsDestroyAPIView(DestroyAPIView):
    """Контроллер удаления одного документа"""

    serializer_class = DocsSerializer
    queryset = Upload.objects.all()
    # permission_classes = [IsAuthenticated,]
    permission_classes = [IsOwner]


class FileDownloadView(APIView):
    permission_classes = [IsOwnerOrSuperUser]

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

