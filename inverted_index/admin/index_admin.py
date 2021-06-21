from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Case, When, Value, FloatField
from django.utils.html import format_html

from inverted_index.enums import INDEX_TYPE_PARAGRAPH, INDEX_TYPE_LINE, COLOR_RED
from inverted_index.models import Paragraph, Line
from inverted_index.services.search_keywords import search_words_exact, sort_based_on_repeat_average
from utility.text_formatting import make_colorful_parts, get_text_html_div, make_bold_parts, make_colorful_bold_parts


class IndexAdmin(ModelAdmin):
    list_display = ['index', 'notebook', 'get_text']
    fields = ['id', 'index', 'get_text', 'notebook']
    list_display_links = ['index']
    readonly_fields = fields
    index_type = None
    search_fields = ['id']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super(IndexAdmin, self).get_search_results(request, queryset, search_term)
        keywords = search_term.split(' ')
        key_ids, index_ids = search_words_exact(index_type=self.index_type, keywords=keywords)
        queryset = queryset.filter(id__in=index_ids)
        indices_with_average_repeats = sort_based_on_repeat_average(key_ids, index_ids)
        whens = []
        for index_id, avg_repeat in indices_with_average_repeats.items():
            whens.append(
                When(
                    id=index_id,
                    then=Value(avg_repeat, output_field=FloatField())
                )
            )
        queryset = queryset.annotate(
            average_repeat=Case(
                *whens,
                default=0,
                output_field=FloatField()
            )
        ).order_by(
            '-average_repeat'
        )
        return queryset, False

    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        return super().changelist_view(request, *args, **kwargs)

    def get_text(self, obj):
        request = getattr(self, 'request', None)
        keywords = []
        if request:
            query_params = request.GET.get('q', '')
            if query_params:
                keywords = query_params.split(' ')
        text = make_colorful_bold_parts(obj.text, keywords, color=COLOR_RED)

        return format_html(
            get_text_html_div(text=text)
        )

    get_text.short_description = 'متن'


@admin.register(Paragraph)
class ParagraphAdmin(IndexAdmin):
    index_type = INDEX_TYPE_PARAGRAPH


@admin.register(Line)
class LineAdmin(IndexAdmin):
    index_type = INDEX_TYPE_LINE
