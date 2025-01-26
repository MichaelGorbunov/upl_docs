from django.contrib import admin

from docs.models import Upload

# from docs.services import send_message
from docs.tasks import send_email_to_user

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Обработка загруженных документов"

# отключение удаления документов на панели
admin.site.disable_action("delete_selected")


@admin.action(description="Отклонить документы")
def rejected_docs(modeladmin, request, queryset):
    count = 0
    queryset.update(state_file=0)
    for obj in queryset:
        modeladmin.send_notification(
            obj
        )  # Вызов метода send_notification из класса DocsAdmin
        count += 1
    modeladmin.message_user(request, f"Отклонено {count} записи(ей).")


@admin.action(description="Принять документы")
def adopted_docs(modeladmin, request, queryset):
    count = 0
    queryset.update(state_file=1)
    for obj in queryset:
        modeladmin.send_notification(
            obj
        )  # Вызов метода send_notification из класса DocsAdmin
        count += 1
    modeladmin.message_user(request, f"Принято {count} записи(ей).")


@admin.register(Upload)
class DocsAdmin(admin.ModelAdmin):
    list_display = ("id", "file_info", "comment", "state_file", "original_filename")
    list_display_links = ("id", "file_info", "comment")
    list_filter = ["state_file"]
    ordering = ["-created_time", "state_file"]
    actions = [rejected_docs, adopted_docs]

    def send_notification(self, obj):
        # chat_id_owner = obj.owner.tg_chat_id
        email_owner = obj.owner.email
        original_filename = obj.original_filename
        message_from_user = (f"Уважаемый {email_owner}. Изменен документ {original_filename}."
                             f" Его статус: {obj.get_state_file_display()} ")
        # telegramm
        # send_message(message=message_from_user, chat_id=chat_id_owner)
        # email
        send_email_to_user.delay(message_from_user, email_owner)
        # try:
        #     send_message(message=message_from_user, chat_id=chat_id_owner)
        # except Exception as e:
        #     modeladmin.message_user(request, f"Ошибка отправки сообщения {email_owner}: {str(e)}", level='error')

    def file_info(self, obj: Upload):
        return f"Файл {obj.original_filename}"

    def save_model(self, request, obj, form, change):
        self.send_notification(obj)  # Вызов в методе save_model
        super().save_model(request, obj, form, change)
