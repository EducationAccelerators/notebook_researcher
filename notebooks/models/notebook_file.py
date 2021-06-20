from django.db import models

from utility.models import BaseModelNoRecovery
from utility.validators import file_extension_validator_wrapper


class NoteBookFile(BaseModelNoRecovery):
    file = models.FileField(
        upload_to='notebooks/',
        verbose_name='فایل جزوه',
        validators=[file_extension_validator_wrapper('.txt'), ]
    )

    name = models.CharField(
        max_length='256',
        verbose_name='نام جزوه'
    )

    class Meta:
        verbose_name = 'فایل جزوه'
        verbose_name_plural = 'فایل های جزوات'
