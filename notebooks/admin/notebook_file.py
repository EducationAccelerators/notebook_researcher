from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notebooks.models import NotebookFile, Notebook
from utility.text_formatting import jalali_strftime


@admin.register(NotebookFile)
class NotebookFileAdmin(ModelAdmin):
    list_display = ['id', 'name', 'get_jalali_created']

    list_display_links = ['name']

    fields = ['id', 'name', 'get_jalali_created', 'file']
    readonly_fields = ['get_jalali_created']

    def get_jalali_created(self, obj):
        return jalali_strftime(obj.created)

    get_jalali_created.short_description = 'تاریخ ساخت'


@admin.register(Notebook)
class NotebookAdmin(ModelAdmin):
    list_display = ['id', 'get_name', 'get_jalali_created', 'get_preview_text']

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def get_preview_text(self, obj):
        return obj.get_preview_text

    get_preview_text.short_description = 'پیش‌نمایش'

    def get_jalali_created(self, obj):
        return jalali_strftime(obj.created)

    get_jalali_created.short_description = 'تاریخ ساخت'

    def get_name(self, obj):
        return obj.name

    get_name.short_description = 'نام جزوه'
