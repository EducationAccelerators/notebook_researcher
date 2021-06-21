from django.contrib import admin
from django.contrib.admin import ModelAdmin

from inverted_index.models import Paragraph, Line


class IndexAdmin(ModelAdmin):
    list_display = ['id', 'index', 'notebook']
    fields = ['id', 'index', 'text', 'notebook']
    readonly_fields = fields

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Paragraph)
class ParagraphAdmin(IndexAdmin):
    pass


@admin.register(Line)
class LineAdmin(IndexAdmin):
    pass
