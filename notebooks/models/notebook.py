from django.db import models

from utility.models import BaseModel


class NoteBook(BaseModel):

    file = models.OneToOneField(
        to='NoteBookFile',
        on_delete=models.PROTECT,
        related_name='notebook',
        verbose_name='فایل جزوه'
    )

    text = models.TextField(
        verbose_name='متن جزوه'
    )

    class Meta:
        verbose_name = 'جزوه'
        verbose_name_plural = 'جزوات'
