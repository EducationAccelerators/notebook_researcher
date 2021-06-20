from django.db import models

from utility.models import BaseModel


class LineInterface(BaseModel):
    line = models.ForeignKey(
        to='Line',
        on_delete=models.CASCADE,
        related_name='interfaces',
        verbose_name='خط مربوطه'
    )

    key = models.ForeignKey(
        to='SearchKey',
        on_delete=models.CASCADE,
        related_name='line_interfaces',
        verbose_name='کلید مربوطه'
    )

    class Meta:
        verbose_name = 'میانی خطی'
        verbose_name_plural = 'میانی های خطی'
