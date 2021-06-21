from django.db import models

from utility.models import BaseModel


class IndexInterface(BaseModel):
    index = models.ForeignKey(
        to='Index',
        on_delete=models.CASCADE,
        related_name='interfaces',
        verbose_name='اندیس مربوطه'
    )

    key = models.ForeignKey(
        to='SearchKey',
        on_delete=models.CASCADE,
        related_name='index_interfaces',
        verbose_name='کلید مربوطه'
    )

    repeat = models.PositiveIntegerField(
        verbose_name='تعداد تکرار',
        default=1
    )

    class Meta:
        verbose_name = 'میانی اندیس'
        verbose_name_plural = 'میانی های اندیس'
