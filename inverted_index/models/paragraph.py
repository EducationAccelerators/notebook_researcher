from inverted_index.enums import INDEX_TYPE_PARAGRAPH
from inverted_index.models import Index


class Paragraph(Index):

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.index_type = INDEX_TYPE_PARAGRAPH
        super(Paragraph, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'پاراگراف'
        verbose_name_plural = 'پاراگراف‌ها'
