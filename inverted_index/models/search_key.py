import re

from django.db import models

from notebooks.models import NotebookElementMixin
from utility.models import BaseModel


class SearchKey(NotebookElementMixin, BaseModel):
    word = models.CharField(
        verbose_name='کلمه کلیدی',
        max_length=1024
    )

    @property
    def is_single_word(self):
        return re.match(r'^\S+$', self.word) is not None

    @property
    def lines(self):
        from inverted_index.models import Line
        return Line.active_objects.filter(
            interfaces__key_id=self.id
        )

    @property
    def paragraphs(self):
        from inverted_index.models import Paragraph
        return Paragraph.active_objects.filter(
            interfaces__key_id=self.id
        )

    class Meta:
        verbose_name = 'کلید جستجو'
        verbose_name_plural = 'کلید های جستجو'
        unique_together = ('word', 'notebook',)
