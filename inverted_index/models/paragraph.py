from django.db import models

from notebooks.models import NotebookElementMixin
from utility.models import BaseModel


class Paragraph(NotebookElementMixin, BaseModel):
    text = models.TextField(
        verbose_name='متن',
    )

    class Meta:
        verbose_name = 'پاراگراف'
        verbose_name_plural = 'پاراگراف‌ها'
