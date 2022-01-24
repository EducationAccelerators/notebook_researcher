from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

from inverted_index.enums import INDEX_TYPE_PARAGRAPH, INDEX_TYPE_LINE, COLOR_RED
from inverted_index.models import Paragraph, Line
from inverted_index.notebook_searcher import ExactKeySearcher, ContainsKeySearcher, IndexSearcher
from notebooks.models import Notebook
from utility.admin import SimpleFilterWithDefaultValue
from utility.text_formatting import get_text_html_div, make_colorful_bold_parts


class SearchTypeFilter(SimpleFilterWithDefaultValue):
    title = 'نوع سرچ'
    parameter_name = 'search_type'

    lookups_field = [
        ('exact', 'خود کلمه'),
        ('contains', 'تطابق کلمه'),
        ('index', 'شماره اندیس')
    ]

    lookup2searcher = {
        lookups_field[0][0]: ExactKeySearcher,
        lookups_field[1][0]: ContainsKeySearcher,
        lookups_field[2][0]: IndexSearcher
    }

    default_value = lookups_field[0][0]

    @classmethod
    def get_search_type_from_request(cls, request):
        return request.GET.get('search_type', cls.default_value)

    @classmethod
    def get_searcher_from_request(cls, request):
        return cls.lookup2searcher.get(cls.get_search_type_from_request(request))

    def get_default_value(self):
        return self.default_value

    def lookups(self, request, model_admin):
        return self.lookups_field

    def queryset(self, request, queryset):
        return queryset


class NotebookFilter(SimpleFilterWithDefaultValue):

    title = 'جزوه'
    parameter_name = 'notebook_filter'

    maximum_notebooks_in_filter = 10

    @staticmethod
    def get_lookups():
        notebooks = list(Notebook.active_objects.order_by('-created')[:min(Notebook.active_objects.count(), 10)])
        lookups = []
        for notebook in notebooks:
            lookups.append(
                (notebook.id, str(notebook))
            )
        return lookups

    def lookups(self, request, model_admin):
        return self.get_lookups()

    def get_default_value(self):
        return str(self.get_lookups()[0][0])

    def queryset(self, request, queryset):
        value = self.get_default_value()
        if self.value():
            value = self.value()
        notebook_id = int(value)
        queryset = queryset.filter(notebook_id=notebook_id)
        return queryset


class IndexAdmin(ModelAdmin):
    list_display = ['index', 'notebook', 'get_text']
    fields = ['id', 'index', 'get_text', 'notebook']
    list_display_links = ['index']
    readonly_fields = fields
    index_type = None
    search_fields = ['id']
    list_filter = [
        SearchTypeFilter,
        NotebookFilter,
    ]
    search_splitter = ' '

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return super(IndexAdmin, self).get_search_results(request, queryset, search_term)
        try:
            searcher = SearchTypeFilter.get_searcher_from_request(request)(
                index_type=self.index_type,
                searched_items=search_term.split(self.search_splitter),
                queryset=queryset,
            )
            return searcher.get_queryset(), False
        except ValueError as e:
            messages.add_message(request, messages.ERROR, 'مقدار سرچ شده منطقی نیست.')
            return queryset, False

    def changelist_view(self, request, *args, **kwargs):
        self.request = request
        return super().changelist_view(request, *args, **kwargs)

    def get_text(self, obj):
        request = getattr(self, 'request', None)
        keywords = []
        text = obj.text
        if request:
            query_params = request.GET.get('q', '')
            if query_params:
                keywords = query_params.split(' ')
            search_type = SearchTypeFilter.get_search_type_from_request(request)
            text = make_colorful_bold_parts(text, keywords, color=COLOR_RED, exact=search_type == 'exact')

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
