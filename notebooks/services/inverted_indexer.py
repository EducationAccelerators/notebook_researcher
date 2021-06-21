# notebook -> inverted_index_model
from inverted_index.models import Index, IndexInterface, SearchKey
from notebooks.enums import PARAGRAPH_SEPARATOR, LINE_SEPARATOR, WORD_SEPARATOR, SEPARATOR_TO_INDEX


def add_index_to_key(key, index):
    interface, created = IndexInterface.active_objects.get_or_create(
        key=key,
        index=index
    )
    if not created:
        interface.repeat += 1
        interface.save(update_fields=['repeat', ])
    return interface


def create_index(text, index, index_type, notebook):
    index_class = Index.index_type2index_class_dict[index_type]
    index, _ = index_class.active_objects.get_or_create(
        index=index,
        notebook=notebook,
        defaults={
            'text': text,
        }
    )
    return index


def create_search_key(keyword, notebook):
    key, _ = SearchKey.active_objects.get_or_create(
        word=keyword,
        notebook=notebook
    )
    return key


def dictor(text, separator, notebook):
    lines = text.split(separator)
    index_type = dict(SEPARATOR_TO_INDEX)[separator]
    for index, line in enumerate(lines):
        index = create_index(line, index, notebook=notebook, index_type=index_type)
        for word in line.split(WORD_SEPARATOR):
            search_key = create_search_key(word, notebook=notebook)
            add_index_to_key(search_key, index)


def inverted_indexer(notebook):
    dictor(text=notebook.text, separator=PARAGRAPH_SEPARATOR, notebook=notebook)
    dictor(text=notebook.text, separator=LINE_SEPARATOR, notebook=notebook)

