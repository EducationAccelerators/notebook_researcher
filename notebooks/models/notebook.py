from django.db import models

from notebooks.enums import PREVIEW_SIZE
from utility.models import BaseModel


class Notebook(BaseModel):
    file = models.OneToOneField(
        to='NotebookFile',
        on_delete=models.PROTECT,
        related_name='notebook',
        verbose_name='فایل جزوه'
    )

    text = models.TextField(
        verbose_name='متن جزوه'
    )

    @property
    def name(self):
        return self.file.name

    @property
    def preview_text(self):
        if len(self.text) <= PREVIEW_SIZE:
            return self.text
        return '{}...'.format(self.text[:PREVIEW_SIZE])

    def __str__(self):
        return '({}): {}'.format(self.id, self.name)

    class Meta:
        verbose_name = 'جزوه'
        verbose_name_plural = 'جزوات'
