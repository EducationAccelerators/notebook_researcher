from django.db import models

from utility.models import BaseModel


class Line(BaseModel):
    text = models.TextField(
        verbose_name='متن',
    )

    class Meta:
        verbose_name = 'خط'
        verbose_name_plural = 'خطوط'
