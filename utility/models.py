import logging

from django.db import models

logger = logging.getLogger(__name__)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)



class BaseModel(models.Model):
    active_objects = ActiveManager()

    objects = models.Manager()

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد',
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ آخرین ویرایش'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='آیا حذف شده است؟'
    )

    is_archived = models.BooleanField(
        default=False,
        verbose_name='آیا آرشیو شده است؟',
    )

    @property
    def meta(self):
        return self._meta

    @property
    def is_create(self):
        return not self.id

    @property
    def is_update(self):
        return not self.is_create

    @property
    def old_instance(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.is_archived = True
        self.save()


class BaseHistoryModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد',
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ آخرین ویرایش'
    )

    @property
    def meta(self):
        return self._meta

    @property
    def is_create(self):
        return not self.id

    @property
    def is_update(self):
        return not self.is_create

    @property
    def old_instance(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    class Meta:
        abstract = True
