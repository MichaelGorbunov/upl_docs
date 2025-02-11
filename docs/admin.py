from django.contrib import admin

from docs.models import Upload
from docs.tasks import send_email_to_user

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Обработка загруженных документов"

# отключение удаления документов на панели
admin.site.disable_action("delete_selected")


@admin.action(description="Отклонить документы")
def rejected_docs(modeladmin, request, queryset):
    count = 0
    # queryset.update(state_file=0)
    for obj in queryset:
        if obj.state_file != 0:
            obj.state_file = 0
            obj.save()
            send_notification(obj)
            count += 1
    modeladmin.message_user(request, f"Отклонено {count} записи(ей).")


@admin.action(description="Принять документы")
def adopted_docs(modeladmin, request, queryset):
    count = 0
    # queryset.update(state_file=1)
    for obj in queryset:
        if obj.state_file != 1:
            obj.state_file = 1
            obj.save()
            send_notification(obj)
            count += 1
    modeladmin.message_user(request, f"Принято {count} записи(ей).")


@admin.register(Upload)
class DocsAdmin(admin.ModelAdmin):
    list_display = ("id", "original_filename", "state_file", "comment")
    list_display_links = ("id", "original_filename", "comment")
    list_filter = ["state_file"]
    ordering = ["-created_time", "state_file"]
    actions = [rejected_docs, adopted_docs]


def send_notification(obj):
    email_owner = obj.owner.email
    original_filename = obj.original_filename
    message_from_user = (
        f"Уважаемый {email_owner}. Изменен документ {original_filename}."
        f" Его статус: {obj.get_state_file_display()} "
    )

    try:
        send_email_to_user.delay(message_from_user, email_owner)
    except Exception as e:
        # Обработка ошибки
        print(
            f"Ошибка при отправке уведомления для {original_filename} ({email_owner}): {str(e)}"
        )
        raise
