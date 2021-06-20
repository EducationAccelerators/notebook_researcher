from django.db import models

from notebooks.models import Notebook


class NotebookElementMixin(models.Model):
    notebook = models.ForeignKey(
        to=Notebook,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='جزوه مربوطه'
    )

    class Meta:
        abstract = True
