from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notebooks.models import NotebookFile
from utility.admin import JalaliCreatedUpdatedMixin


@admin.register(NotebookFile)
class NotebookFileAdmin(JalaliCreatedUpdatedMixin, ModelAdmin):
    list_display = ['id', 'name', 'get_jalali_created']

    list_display_links = ['name']

    fields = ['id', 'name', 'get_jalali_created', 'file']
    readonly_fields = ['get_jalali_created']

    def has_change_permission(self, request, obj=None):
        return False
