from django.urls import path

from docs.apps import DocsConfig
from docs.views import (DocsCreateAPIView,DocsListAPIView)

app_name = DocsConfig.name

urlpatterns = [
    # вывод списка привычек
    path("list/", DocsListAPIView.as_view(), name="docs-list"),
    path("create/", DocsCreateAPIView.as_view(), name="docs-create"),

]