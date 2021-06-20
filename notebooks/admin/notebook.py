from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notebooks.models import Notebook
from utility.admin import JalaliCreatedUpdatedMixin


@admin.register(Notebook)
class NotebookAdmin(JalaliCreatedUpdatedMixin, ModelAdmin):
    list_display = ['get_name', 'get_jalali_created', 'get_preview_text']

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def get_preview_text(self, obj):
        return obj.get_preview_text

    get_preview_text.short_description = 'پیش‌نمایش'

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'نام جزوه'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

