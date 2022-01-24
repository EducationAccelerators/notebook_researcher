from abc import abstractmethod, ABC
from collections import Iterable
from typing import List

from django.db.models import QuerySet


class NotebookSearcher(ABC):
    order_by_field = None

    def __init__(self, index_type: str, searched_items: List[str], queryset):
        self.index_type = index_type
        self.searched_items = searched_items
        self.queryset = queryset

    @abstractmethod
    def get_search_result(self) -> QuerySet:
        pass

    def order_queryset(self, queryset):
        if self.order_by_field is None:
            return queryset
        if isinstance(self.order_by_field, str):
            return queryset.all().order_by(self.order_by_field).all()
        elif isinstance(self.order_by_field, Iterable):
            return queryset.all().order_by(*self.order_by_field).all()
        else:
            return queryset.all().order_by(self.order_by_field).all()

    def get_queryset(self):
        return self.order_queryset(self.get_search_result())
