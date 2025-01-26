from django.contrib import admin
from docs.models import Upload
from docs.services import send_message
from docs.tasks import send_email_to_user
import os

# from django_filters import FilterSet
# admin.site.register(Upload)

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Обработка загруженных документов"

# отключение удаления документов на панели
admin.site.disable_action('delete_selected')


@admin.action(description="Отклонить документы")
def rejected_docs(self, request, queryset):
    for obj in queryset:
        status = obj.id
        chat_id_owner = obj.owner.tg_chat_id
        # self.message_user(request, f" {status} ")
        original_filename = obj.original_filename
        email_owner = obj.owner.email
        message_from_user = f"Уважаемый {email_owner} . Изменен документ {original_filename}. Его статус: {obj.get_state_file_display()} "
        send_message(message=message_from_user, chat_id=chat_id_owner)
    count = queryset.update(state_file=0)
    self.message_user(request, f"Изменено {count} записи(ей).")


@admin.action(description="Принять документы")
def adopted_docs(self, request, queryset):
    for obj in queryset:
        status = obj.id
        chat_id_owner = obj.owner.tg_chat_id
        # self.message_user(request, f" {status} ")
        original_filename = obj.original_filename
        email_owner = obj.owner.email
        message_from_user = f"Уважаемый {email_owner} . Изменен документ {original_filename}. Его статус: {obj.get_state_file_display()} "
        send_message(message=message_from_user, chat_id=chat_id_owner)
    count = queryset.update(state_file=1)
    self.message_user(request, f"Изменено {count} записи(ей).")


@admin.register(Upload)
class DocsAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_info', 'comment', 'state_file', 'original_filename')
    list_display_links = ('id', 'file_info', 'comment')
    list_filter = ['state_file']
    ordering = ['-created_time', 'state_file']
    actions = [rejected_docs, adopted_docs]

    def file_info(self, file_nm: Upload.file):
        return f"Файл {file_nm} "

    def save_model(self, request, obj, form, change):
        # Внесите нужные изменения в объект перед сохранением
        file_name = os.path.basename(obj.file.name)
        chat_id_owner = obj.owner.tg_chat_id
        email_owner = obj.owner.email
        original_filename = obj.original_filename
        message_from_user = f"Уважаемый {email_owner} . Изменен документ {original_filename}. Его статус: {obj.get_state_file_display()} "
        send_message(message=message_from_user, chat_id=chat_id_owner)
        send_email_to_user.delay(message_from_user, email_owner)
        super().save_model(request, obj, form, change)

# class DocsAdminFilter(admin.SimpleListFilter):
#     title = 'Статус документа'
#     parameter_name = 'state_file'
#
#     def lookups(self, request, ModelAdmin):
#         return [
#             (0, 'Отклонен'),
#             (1, 'Принят'),
#             (2, 'На рассмотрении'),
#         ]
#
#     def queryset(self, request, queryset):
#         return queryset
