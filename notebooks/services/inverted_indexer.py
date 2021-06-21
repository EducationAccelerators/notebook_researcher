# notebook -> inverted_index_model
from inverted_index.models import Index, IndexInterface, SearchKey
from notebooks.enums import PARAGRAPH_SEPARATOR, LINE_SEPARATOR, WORD_SEPARATOR, SEPARATOR_TO_INDEX
from utility.text_formatting import clean_meaningless_parts_from_word


def add_index(dict_obj: dict, word, index):
    if word in dict_obj:
        if index in dict_obj[word]:
            dict_obj[word][index] += 1
        else:
            dict_obj[word][index] = 1
    else:
        dict_obj[word] = {
            index: 1
        }


def create_index_interface(key_id, index_id, repeat):
    return IndexInterface.active_objects.create(
        key_id=key_id,
        index_id=index_id,
        repeat=repeat
    )


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
    keyword2indices = {}
    lines = text.split(separator)
    index_type = dict(SEPARATOR_TO_INDEX)[separator]

    index_number2index_id = {}
    for index, line in enumerate(lines):
        index_obj = create_index(line, index, notebook=notebook, index_type=index_type)
        index_number2index_id[index] = index_obj.id

    keyword2search_key_id = {}
    for index, line in enumerate(lines):
        for word in line.split(WORD_SEPARATOR):
            cleaned_word = clean_meaningless_parts_from_word(word)
            if cleaned_word not in keyword2search_key_id:
                search_key = create_search_key(cleaned_word, notebook=notebook)
                keyword2search_key_id[cleaned_word] = search_key.id
            add_index(keyword2indices, cleaned_word, index)

    for keyword, indices in keyword2indices.items():
        for index_number, repeat in indices.items():
            create_index_interface(
                key_id=keyword2search_key_id[keyword],
                index_id=index_number2index_id[index_number],
                repeat=repeat
            )


def inverted_indexer(notebook):
    if notebook.model_created:
        return False

    dictor(text=notebook.text, separator=PARAGRAPH_SEPARATOR, notebook=notebook)
    dictor(text=notebook.text, separator=LINE_SEPARATOR, notebook=notebook)

    notebook.model_created = True
    notebook.save(update_fields=['model_created', ])

    return True
