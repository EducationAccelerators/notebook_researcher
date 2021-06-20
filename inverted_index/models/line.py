from django.db import models

from notebooks.models import NotebookElementMixin
from utility.models import BaseModel


class Line(NotebookElementMixin, BaseModel):
    text = models.TextField(
        verbose_name='متن',
    )

    class Meta:
        verbose_name = 'خط'
        verbose_name_plural = 'خطوط'
