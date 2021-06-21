import re

from jalali_date import datetime2jalali
from tqdm import tqdm


def jalali_strftime(input_datetime, output_format='%H:%M %Y/%m/%d'):
    return datetime2jalali(input_datetime).strftime(output_format)


class PersianEditor:
    misc_non_persian_chars = {
        'bad_chars': ",;كي",
        'good_chars': "،؛کی"
    }

    @classmethod
    def tr(cls, intab, outtab, txt):
        return txt.translate({ord(k): v for k, v in zip(intab, outtab)})

    @classmethod
    def fix_misc_non_persian_chars(cls, text):
        return cls.tr(
            cls.misc_non_persian_chars['bad_chars'],
            cls.misc_non_persian_chars['good_chars'],
            text
        )

    @classmethod
    def remove_incorrect_endlines(cls, text):
        return re.sub(r'(?<!\.)\n', ' ', text)

    @classmethod
    def remove_footnotes(cls, text):
        return re.sub(r'(?<!\s)\d+', '', text)

    @classmethod
    def clean_all_long_words(cls, text):
        return re.sub(r"""ـ+""", "", text)

    @classmethod
    def fix_parentheses(cls, text):
        return cls.tr(
            intab='[]{}()<>',
            outtab='][}{)(><',
            txt=text
        )

    def __init__(self):
        self._formatters = [
            self.fix_misc_non_persian_chars,
            self.remove_incorrect_endlines,
            self.remove_footnotes,
            self.clean_all_long_words,
            self.fix_parentheses
        ]

    def format_all(self, text):
        for i in tqdm(range(len(self._formatters)), desc='farsi formatting'):
            text = self._formatters[i](text)
        return text


def clean_meaningless_parts_from_word(word):
    return re.sub(r"[^\w\s]", '', word)


def make_bold_html(text):
    return '<b>' + text + '</b>'


def make_bold_parts(text, parts):
    for part in parts:
        text = text.replace(part, make_bold_html(part))
    return text


def make_colorful_html(text, color):
    return '<span style="color: {};">{}</span>'.format(
        color,
        text
    )


def make_colorful_parts(text, parts, color):
    for part in parts:
        text = text.replace(part, make_colorful_html(part, color))
    return text


def get_text_html_div(text, style=None):
    text = text.replace('\n', '<br/>')
    if style is None:
        style = 'font-size: 16px; ' \
                'font-family: IRANSans, Helvetica, sans-serif, Georgia, "Times New Roman", Times, serif !important;'
    return '<div style="{style}"><p>{text}</p></div>'.format(
        style=style,
        text=text
    )
