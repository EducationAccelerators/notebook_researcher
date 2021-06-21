from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.utils import timezone

from notebooks.models import Notebook
from notebooks.services.inverted_indexer import inverted_indexer
from utility.admin import JalaliCreatedUpdatedMixin


def created_inverted_index_model(modeladmin, request, queryset):
    created_count = 0
    time_taken = []
    for notebook in queryset:
        t1 = timezone.now()
        created = inverted_indexer(notebook)
        t2 = timezone.now()
        created_count += int(created)
        if created:
            time_taken.append(t2 - t1)

    message_type = messages.SUCCESS if created_count else messages.WARNING
    message = 'تعداد {} مدل از روی {} جزوه ساخته شد.'.format(created_count, len(queryset))
    if created_count:
        total = timezone.timedelta(seconds=0)
        for timedelta in time_taken:
            total += timedelta
        avg = total / len(time_taken)
        message = '{}\n{}'.format(
            message,
            'مدت زمان میانگین ساختن هر مدل: {}\n'
            'مدت زمان کل: {}'.format(
                avg,
                total
            )
        )

    messages.add_message(request, message_type, message)


created_inverted_index_model.short_description = 'ساختن مدل سرچ'


@admin.register(Notebook)
class NotebookAdmin(JalaliCreatedUpdatedMixin, ModelAdmin):
    list_display = ['id', 'get_name', 'get_jalali_created', 'get_list_preview_text']
    fields = ['get_name', 'get_jalali_created', 'get_preview_text', 'text']
    LIST_PREVIEW_SIZE = 128

    actions = [created_inverted_index_model, ]

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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
