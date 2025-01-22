from django.db import models

from config import settings

# Create your models here.
NULLABLE = {"blank": True, "null": True}


class Upload(models.Model):
    class State(models.IntegerChoices):
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

    filename = models.CharField(
        max_length=150, verbose_name="Имя файла", help_text="File name", **NULLABLE
    )

    file = models.FileField(upload_to='upload'
    )

    hash_file = models.CharField(
        max_length=150, verbose_name="Хэш файла", help_text="File hash", **NULLABLE
    )
    state_file = models.SmallIntegerField( choices=State.choices, default=State.awaiting)

    created_time = models.DateTimeField(verbose_name="Время создания", auto_now=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["created_time"]
