from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import CustomUser
from users.permissions import IsAccountOwner
from users.serializer import CustomUserDetailSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления профилем пользователя.
    Позволяет:
    - Создавать пользователей (доступно для всех).
    - Получать и изменять только свои собственные данные (требуется аутентификация).
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # Базовый сериализатор
    permission_classes = [IsAuthenticated]  # Общие разрешения по умолчанию

    def get_permissions(self):
        """
        Возвращает список разрешений в зависимости от действия.
        """
        if self.action == "create":  # Создание пользователя
            return [AllowAny()]  # Доступно для всех
        elif self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [IsAccountOwner()]  # Только владелец
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Хеширует пароль пользователя перед созданием.
        """
        # Создаём пользователя
        user = serializer.save()
        user.set_password(user.password)  # Хешируем пароль
        user.is_active = True  # Установить активным по умолчанию
        user.save()

    def get_serializer_class(self):
        """
        Устанавливает сериализатор:
        - Детальный сериализатор, если это владелец.
        - Базовый сериализатор в остальных случаях.
        """
        # Если действие связано с владельцем, возвращаем CustomUserDetailSerializer
        if self.action in ["retrieve", "update", "partial_update"]:
            return CustomUserDetailSerializer

        # По умолчанию используется базовый сериализатор
        return super().get_serializer_class()
