from functools import reduce
from operator import and_

from inverted_index.enums import INDEX_TYPE_PARAGRAPH
from inverted_index.models import SearchKey, IndexInterface
from utility.python import Set


def search_words(index_type, keywords):
    search_keys = SearchKey.active_objects.filter(word__in=keywords)
    if search_keys.count() != len(keywords):
        return search_keys.values_list('id', flat=True), set()
    property_name = 'paragraphs' if index_type == INDEX_TYPE_PARAGRAPH else 'lines'
    index_ids = reduce(and_, [
        Set(getattr(key, property_name).values_list('id', flat=True)) for key in search_keys
    ])
    return search_keys.values_list('id', flat=True), index_ids


def sort_based_on_repeat_average(search_keys_ids, index_ids):
    indices_with_repeats = {}

    def average(array):
        return sum(array)/len(array)

    for index_id in index_ids:
        indices_with_repeats[index_id] = IndexInterface.active_objects.filter(
            index_id=index_id,
            key_id__in=search_keys_ids
        ).values_list('repeat', flat=True)

    indices_with_average_repeats = {
        index_id: average(repeats) for index_id, repeats in indices_with_repeats.items()
    }

    return indices_with_average_repeats
