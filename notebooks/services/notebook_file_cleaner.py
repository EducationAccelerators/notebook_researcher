# notebookFile -> noteBook

def omit_fake_spaces(text: str):
    text = text.replace('.\n', '@')
    text = text.replace('\n', '')
    return text.replace('@', '.\n')


def fix_encode_characters(text):
    # todo ask for ashkan's help for changing [ی و ک و ...]
    return text


def notebook_file_cleaner(notebook_file):
    text = notebook_file.file.read()
    text = omit_fake_spaces(text)
    text = fix_encode_characters(text)
    # todo Create A NoteBook Based On Text And File
    pass
