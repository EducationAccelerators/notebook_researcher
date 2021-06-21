from django.db import models

from inverted_index.enums import INDEX_TYPES, INDEX_TYPE_PARAGRAPH, INDEX_TYPE_LINE, PREVIEW_SIZE
from notebooks.models import NotebookElementMixin
from utility.models import BaseModel
from utility.python import classproperty


class Index(NotebookElementMixin, BaseModel):
    text = models.TextField(
        verbose_name='متن',
    )

    index = models.PositiveIntegerField(
        verbose_name='شماره اندیس'
    )

    index_type = models.CharField(
        verbose_name='نوع اندیس',
        choices=INDEX_TYPES,
        max_length=512
    )

    @property
    def try_line(self):
        from inverted_index.models import Line
        if isinstance(self, Line):
            return self
        try:
            return self.line
        except:
            return None

    @property
    def try_paragraph(self):
        from inverted_index.models import Paragraph
        if isinstance(self, Paragraph):
            return self
        try:
            return self
        except:
            return None

    @property
    def concrete_instance(self):
        return self.try_line or self.try_paragraph

    @classproperty
    def index_type2index_class_dict(cls):
        from inverted_index.models import Paragraph, Line
        return {
            INDEX_TYPE_PARAGRAPH: Paragraph,
            INDEX_TYPE_LINE: Line
        }

    @property
    def preview(self):
        if len(self.text) < PREVIEW_SIZE:
            return self.text
        return self.text[:PREVIEW_SIZE]

    def __str__(self):
        return self.preview

    class Meta:
        verbose_name = 'اندیس'
        verbose_name_plural = 'اندیس‌ها'
        unique_together = (
            'index', 'index_type', 'notebook'
        )
