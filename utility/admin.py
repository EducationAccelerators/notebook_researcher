from abc import abstractmethod, ABC

from django.contrib.admin import SimpleListFilter
from django.utils.encoding import force_text

from utility.text_formatting import jalali_strftime


class JalaliCreatedUpdatedMixin:

    def get_jalali_created(self, obj):
        return jalali_strftime(obj.created)

    get_jalali_created.short_description = 'تاریخ ساخت'
    get_jalali_created.admin_order_field = 'created'

    def get_jalali_updated(self, obj):
        return jalali_strftime(obj.updated)

    get_jalali_updated.short_description = 'تاریخ آخرین تغییر'
    get_jalali_updated.admin_order_field = 'updated'


class SimpleFilterWithDefaultValue(ABC, SimpleListFilter):

    @abstractmethod
    def get_default_value(self):
        return

    def get_value(self):
        return self.value() or self.get_default_value()

    def choices(self, changelist):
        """
        Overwrite this method to prevent the default "All".
        """
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.get_value() == force_text(lookup),
                'query_string': changelist.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }
