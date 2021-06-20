from django.db import models

from notebooks.models import NoteBook


class NotebookElementMixin(models.Model):
    notebook = models.ForeignKey(
        to=NoteBook,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='جزوه مربوطه'
    )

    class Meta:
        abstract = True
