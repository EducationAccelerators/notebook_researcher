from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notebooks.models import Notebook
from utility.admin import JalaliCreatedUpdatedMixin


@admin.register(Notebook)
class NotebookAdmin(JalaliCreatedUpdatedMixin, ModelAdmin):
    list_display = ['id', 'get_name', 'get_jalali_created', 'get_list_preview_text']
    fields = ['get_name', 'get_jalali_created', 'get_preview_text']
    LIST_PREVIEW_SIZE = 32

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def get_preview_text(self, obj):
        return obj.preview_text

    get_preview_text.short_description = 'پیش‌نمایش'

    def get_list_preview_text(self, obj):
        if len(obj.preview_text) <= self.LIST_PREVIEW_SIZE:
            return obj.preview_text
        return '{}...'.format(obj.text[:self.LIST_PREVIEW_SIZE])

    get_list_preview_text.short_description = 'پیش‌نمایش'

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'نام جزوه'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
