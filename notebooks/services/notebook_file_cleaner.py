# notebookFile -> noteBook
from notebooks.models import NotebookFile, Notebook
from utility.text_formatting import PersianEditor


def create_cleaned_notebook_from_notebook_file(notebook_file: NotebookFile):
    text = notebook_file.file.file.read().decode('utf-8', errors='ignore')
    editor = PersianEditor()
    text = editor.format_all(text)
    return Notebook.active_objects.get_or_create(
        notebook_file=notebook_file,
        defaults={
            'text': text
        }
    )
