import re

from jalali_date import datetime2jalali


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

    def __init__(self):
        self._formatters = [
            self.fix_misc_non_persian_chars,
            self.remove_incorrect_endlines,
            self.remove_footnotes,
            self.clean_all_long_words,
        ]

    def format_all(self, text):
        for formatter in self._formatters:
            text = formatter(text)
        return text


def clean_meaningless_parts_from_word(word):
    return re.sub(r"[^\w\s]", '', word)
