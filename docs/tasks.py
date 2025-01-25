from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from docs.models import Upload



@shared_task
def send_email_to_user(message,email):
    """Функция отправки сообщения об обновлении документа."""

    send_mail(
        subject="Обновление статуса загруженного документа ",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

@shared_task
def send_email_to_admin(message):
    """Функция отправки сообщения загрузке документа."""

    send_mail(
        subject="Загружен новый документ",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ADMIN_EMAIL],
    )
