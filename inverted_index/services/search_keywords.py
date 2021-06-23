from collections import Iterable
from functools import reduce
from operator import and_, or_

from inverted_index.enums import INDEX_TYPE_PARAGRAPH
from inverted_index.models import SearchKey, IndexInterface
from utility.python import Set


def search_words_exact(index_type, keywords, notebook_ids: Iterable = None):
    search_keys = SearchKey.active_objects.filter(word__in=keywords)
    if notebook_ids:
        search_keys = search_keys.filter(notebook_id__in=notebook_ids)
    if search_keys.count() != len(keywords):
        return search_keys.values_list('id', flat=True), set()
    property_name = 'paragraphs' if index_type == INDEX_TYPE_PARAGRAPH else 'lines'
    index_ids = reduce(and_, [
        Set(getattr(key, property_name).values_list('id', flat=True)) for key in search_keys
    ])
    return search_keys.values_list('id', flat=True), index_ids


def search_words_contains(index_type, keywords, notebook_ids: Iterable = None):
    property_name = 'paragraphs' if index_type == INDEX_TYPE_PARAGRAPH else 'lines'
    new_indices_list = []
    keys_set = Set()
    for keyword in keywords:
        contained_keys = SearchKey.active_objects.filter(word__contains=keyword)
        if notebook_ids:
            contained_keys = contained_keys.filter(notebook_id__in=notebook_ids)
        keys_set = keys_set.union(Set(list(contained_keys.values_list('id', flat=True))))
        if contained_keys:
            new_indices_list.append(reduce(or_, [
                Set(getattr(key, property_name).values_list('id', flat=True)) for key in contained_keys
            ]))
    index_ids = []
    if new_indices_list:
        index_ids = reduce(and_, new_indices_list)
    return keys_set, index_ids


def sort_based_on_repeat_average(search_keys_ids, index_ids):
    indices_with_repeats = {}

    def average(array):
        return sum(array) / len(array)

    for index_id in index_ids:
        indices_with_repeats[index_id] = IndexInterface.active_objects.filter(
            index_id=index_id,
            key_id__in=search_keys_ids
        ).values_list('repeat', flat=True)

    indices_with_average_repeats = {
        index_id: average(repeats) for index_id, repeats in indices_with_repeats.items()
    }

    return indices_with_average_repeats
