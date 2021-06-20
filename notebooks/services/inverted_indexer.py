# notebook -> inverted_index_model
line_separator = '.'
paragraph_separator = '\n'
word_separator = ' '


def add_index(dict_obj: dict, word, index):
    if word in dict_obj:
        if index in dict_obj[word]:
            dict_obj[word][index] += 1
        else:
            dict_obj[word][index] = 1
    else:
        dict_obj[word] = [index]


def dictor(text, separator):
    dictor_obj = {}
    lines = text.split(line_separator)
    for index, line in enumerate(lines):
        for word in line.split(word_separator):
            add_index(dictor_obj, word, index)
    return dictor_obj, lines


def inverted_indexer(notebook):
    text = notebook.text
    paragraph_hash, paragraphs = dictor(text=notebook.text, separator=paragraph_separator)
    line_hash, lines = dictor(text=notebook.text, separator=line_separator)
    # lines & Paragraphs hashes and weights are ready. Need To Create Objects (line_hash[word][index] = weight)
    # todo Create Search_keys, lines+interfaces, paragraphs+interfaces

