from inverted_index.enums import INDEX_TYPE_LINE
from inverted_index.models import Index


class Line(Index):

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.index_type = INDEX_TYPE_LINE
        super(Line, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'خط'
        verbose_name_plural = 'خطوط'
