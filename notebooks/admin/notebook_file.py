from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.utils import timezone

from notebooks.models import NotebookFile
from notebooks.services.notebook_file_cleaner import create_cleaned_notebook_from_notebook_file
from utility.admin import JalaliCreatedUpdatedMixin


def make_corresponding_notebooks(modeladmin, request, queryset):
    created_count = 0
    time_taken = []
    for notebook_file in queryset:
        t1 = timezone.now()
        notebook, created = create_cleaned_notebook_from_notebook_file(notebook_file)
        t2 = timezone.now()
        created_count += int(created)
        if created:
            time_taken.append(t2 - t1)

    message_type = messages.SUCCESS if created_count else messages.WARNING
    message = 'تعداد {} جزوه از روی {} فایل ساخته شد.'.format(created_count, len(queryset))
    if created_count:
        total = timezone.timedelta(seconds=0)
        for timedelta in time_taken:
            total += timedelta
        avg = total / len(time_taken)
        message = '{}\n{}'.format(
            message,
            'مدت زمان میانگین ساختن هر جزوه: {}\n'
            'مدت زمان کل: {}'.format(
                avg,
                total
            )
        )

    messages.add_message(request, message_type, message)


make_corresponding_notebooks.short_description = 'ساختن جزوه متناظر با فایل'


@admin.register(NotebookFile)
class NotebookFileAdmin(JalaliCreatedUpdatedMixin, ModelAdmin):
    list_display = ['id', 'name', 'get_jalali_created']

    list_display_links = ['name']

    fields = ['name', 'get_jalali_created', 'file']
    readonly_fields = ['get_jalali_created']

    actions = [
        make_corresponding_notebooks
    ]

    def has_change_permission(self, request, obj=None):
        return False
