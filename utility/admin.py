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



