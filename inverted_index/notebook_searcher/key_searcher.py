from abc import ABC, abstractmethod

from django.db.models import QuerySet, When, FloatField, Value, Case

from inverted_index.notebook_searcher import NotebookSearcher
from inverted_index.services.search_keywords import sort_based_on_repeat_average, search_words_exact, \
    search_words_contains


class KeySearcher(NotebookSearcher, ABC):
    order_by_field = '-average_repeat'

    @abstractmethod
    def get_searcher_function(self) -> callable: pass

    def get_search_result(self) -> QuerySet:
        key_ids, index_ids = self.get_searcher_function()(
            self.index_type,
            self.searched_items,
            notebook_ids=set(self.queryset.values_list('notebook', flat=True)),
        )
        queryset = self.queryset.filter(id__in=index_ids)
        indices_with_average_repeats = sort_based_on_repeat_average(key_ids, index_ids)
        whens = []
        for index_id, avg_repeat in indices_with_average_repeats.items():
            whens.append(
                When(
                    id=index_id,
                    then=Value(avg_repeat, output_field=FloatField())
                )
            )
        return queryset.annotate(
            average_repeat=Case(
                *whens,
                default=0,
                output_field=FloatField()
            )
        )


class ExactKeySearcher(KeySearcher):
    def get_searcher_function(self) -> callable:
        return search_words_exact


class ContainsKeySearcher(KeySearcher):
    def get_searcher_function(self) -> callable:
        return search_words_contains
