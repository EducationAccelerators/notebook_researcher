from django.contrib import admin
from django.contrib.admin import ModelAdmin

from inverted_index.models import SearchKey


@admin.register(SearchKey)
class SearchKeyAdmin(ModelAdmin):
    list_display = ['word', 'get_is_single_word', 'notebook']
    fields = list_display
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
