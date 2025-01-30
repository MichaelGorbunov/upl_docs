from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_type(file):
    """Валидатор для проверки типа файла."""
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise ValidationError(
            f"Не поддерживаемый тип файлов: {file.content_type}. "
            f'Разрешенные типы файлов: {", ".join(settings.ALLOWED_FILE_TYPES)}'
        )


def validate_file_size(file):
    """Валидатор для проверки размера файла."""
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"Размер файла не должен превышать {settings.MAX_UPLOAD_SIZE / (1024 * 1024):.2f} MB."
            f" Размер вашего файла {file.size / (1024 * 1024):.2f} MB."
        )
