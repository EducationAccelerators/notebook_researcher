from django.db import models

from utility.models import BaseModel


class Paragraph(BaseModel):
    text = models.TextField(
        verbose_name='متن',
    )

    class Meta:
        verbose_name = 'پاراگراف'
        verbose_name_plural = 'پاراگراف‌ها'
