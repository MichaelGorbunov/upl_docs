from django.urls import path

from docs.apps import DocsConfig
from docs.views import (DocsCreateAPIView, DocsListAPIView, DocsDestroyAPIView, FileDownloadView)

app_name = DocsConfig.name

urlpatterns = [
    # вывод списка документов
    path("list/", DocsListAPIView.as_view(), name="docs-list"),
    #создание документа
    path("create/", DocsCreateAPIView.as_view(), name="docs-create"),
    # удаление одного документа
    path("delete/<int:pk>/", DocsDestroyAPIView.as_view(), name="docs-delete"),
    #скачивание файла
    path('download/<int:pk>/', FileDownloadView.as_view(), name='file-download'),

]