from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_type(file):
    """Валидатор для проверки типа файла."""
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise ValidationError(f'Не поддерживаемый тип файлов: {file.content_type}. Разрешенные типы файлов: {", ".join(settings.ALLOWED_FILE_TYPES)}')