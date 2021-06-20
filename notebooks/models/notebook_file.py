from django.db import models

from notebooks.enums import NOTEBOOK_VALID_FILE_EXTENSIONS
from utility.models import BaseHistoryModel


def validate_txt_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    valid_extensions = NOTEBOOK_VALID_FILE_EXTENSIONS.copy()
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in valid_extensions:
        if len(valid_extensions) == 1:
            message = 'تنها پسوند مجاز {} می‌باشد.'.format(valid_extensions[0])
        else:
            message = 'تنها می‌توانید فایل با با پسوند های {} را آپلود کنید.'.format(str(valid_extensions))
        raise ValidationError(message)


class NoteBookFile(BaseHistoryModel):
    file = models.FileField(
        upload_to='notebooks/',
        verbose_name='فایل جزوه',
        validators=[validate_txt_file_extension, ]
    )

    name = models.CharField(
        max_length=256,
        verbose_name='نام جزوه'
    )

    class Meta:
        verbose_name = 'فایل جزوه'
        verbose_name_plural = 'فایل های جزوات'
