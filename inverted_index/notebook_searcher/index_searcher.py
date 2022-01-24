from django.db.models import QuerySet

from inverted_index.notebook_searcher import NotebookSearcher


class IndexSearcher(NotebookSearcher):
    order_by_field = 'index'

    def get_indices_out_of_searched_items(self):
        indices = []
        for index in self.searched_items:
            indices.append(int(index))
        return indices

    def get_search_result(self) -> QuerySet:
        return self.queryset.filter(
            index__in=self.get_indices_out_of_searched_items()
        )
