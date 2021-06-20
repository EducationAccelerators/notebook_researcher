from django.db import models

from utility.models import BaseModel


class ParagraphInterface(BaseModel):
    paragraph = models.ForeignKey(
        to='Paragraph',
        on_delete=models.CASCADE,
        related_name='interfaces',
        verbose_name='پاراگراف مربوطه'
    )

    key = models.ForeignKey(
        to='SearchKey',
        on_delete=models.CASCADE,
        related_name='key',
        verbose_name='کلید مربوطه'
    )

    repeat = models.PositiveIntegerField(
        verbose_name='تعداد تکرار',
        default=1
    )

    class Meta:
        verbose_name = 'میانی پاراگرافی'
        verbose_name_plural = 'میانی های پاراگرافی'
