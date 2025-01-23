from django.contrib import admin
from docs.models import Upload

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
