# urls.py
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import CustomUserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")


urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path("token_refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
