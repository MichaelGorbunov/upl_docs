from config import settings
# import os
from django.db import models
# from datetime import datetime
# import hashlib

# Create your models here.
NULLABLE = {"blank": True, "null": True}


class Upload(models.Model):
    class State(models.IntegerChoices):
        '''класс для выбора состояния документа'''
        rejected = 0, 'Документ отклонен'
        adopted = 1, 'Документ принят'
        awaiting = 2, 'Докумен на проверке'

    # STATE_CHOICES = [
    #     (0, 'Документ отклонен'),
    #     (1, 'Документ принят'),
    #     (2, 'Докумен на проверке'),
    # ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="укажите владельца",
    )
    comment = models.CharField(
        max_length=150, verbose_name="Комментарий к документу", help_text="Comment for doc", **NULLABLE
    )

    original_filename = models.CharField(
        max_length=150, verbose_name="Имя файла", help_text="File name", **NULLABLE
    )

    file = models.FileField(upload_to='upload'
                            )

    hash_file = models.CharField(
        max_length=32, verbose_name="Хэш файла", help_text="File hash", **NULLABLE
    )
    state_file = models.SmallIntegerField(choices=State.choices, default=State.awaiting)

    created_time = models.DateTimeField(verbose_name="Время создания", auto_now=True)

    def __str__(self):
        '''string for docs record'''
        return self.file.name

    def delete(self, *args, **kwargs):
        '''delete docs record'''
        # До удаления записи получаем необходимую информацию
        storage, path = self.file.storage, self.file.path
        # удаляем сам файл storage.delete(path)
        storage.delete(path)
        super(Upload, self).delete(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Сохраняем имя файла, если файл был загружен
    #     if self.file:
    #         self.hash_file = self.calculate_md5(self.file)
    #         # Получаем оригинальное имя файла до его переименования
    #         original_name = self.file.name
    #         # Получаем текущее время в нужном формате
    #         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #         # Получаем имя файла без расширения
    #         base_name, extension = os.path.splitext(original_name)
    #         # Формируем новое имя файла с меткой времени
    #         new_filename = f"{timestamp}{extension}"
    #         # Сохраняем оригинальное имя файла
    #         self.original_filename = original_name
    #         # Устанавливаем новое имя файла
    #         self.file.name = new_filename
    #     super(Upload, self).save(*args, **kwargs)
    #
    # def calculate_md5(self, file):
    #     """Вычисляет MD5-хэш для файла."""
    #     hash_md5 = hashlib.md5()
    #     # Считываем файл по частям
    #     for chunk in file.chunks():  # Используем метод chunks для считывания файла
    #         hash_md5.update(chunk)
    #
    #     return hash_md5.hexdigest()


    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["created_time"]
