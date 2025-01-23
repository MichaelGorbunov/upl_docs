from django.urls import path

from docs.apps import DocsConfig
from docs.views import (DocsCreateAPIView,DocsListAPIView,DocsDestroyAPIView)

app_name = DocsConfig.name

urlpatterns = [
    # вывод списка документов
    path("list/", DocsListAPIView.as_view(), name="docs-list"),
    #создание документа
    path("create/", DocsCreateAPIView.as_view(), name="docs-create"),
    # удаление одного документа
    path("<int:pk>/delete/", DocsDestroyAPIView.as_view(), name="docs-delete"),

]