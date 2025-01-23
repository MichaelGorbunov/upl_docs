from django.contrib import admin
from docs.models import Upload
from docs.services import send_message
import os

# from django_filters import FilterSet
# admin.site.register(Upload)

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Обработка загруженных документов"

#отключение удаления документов на панели
admin.site.disable_action('delete_selected')

@admin.action(description="Отклонить документы")
def rejected_docs(self, request, queryset):
    count = queryset.update(state_file=0)
    self.message_user(request, f"Изменено {count} записи(ей).")


@admin.action(description="Принять документы")
def adopted_docs(self, request, queryset):
    count = queryset.update(state_file=1)
    self.message_user(request, f"Изменено {count} записи(ей).")


@admin.register(Upload)
class DocsAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_info', 'comment', 'state_file')
    list_display_links = ('id', 'file_info', 'comment')
    list_filter = ['state_file']
    ordering = ['-created_time', 'state_file']
    actions = [rejected_docs, adopted_docs]

    def file_info(self, file_nm: Upload.file):
        return f"Файл {file_nm} "

    def save_model(self, request, obj, form, change):
        # Внесите нужные изменения в объект перед сохранением
        file_name=os.path.basename(obj.file.name)
        chat_id_owner = obj.owner.tg_chat_id
        email_owner = obj.owner.email
        send_message(message=f"Уважаемый {email_owner }Изменен документ {file_name} ",chat_id=chat_id_owner)
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
