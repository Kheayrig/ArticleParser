import json
from enum import Enum


class Brackets(Enum):
    none = '', '',
    round = '(', ')',
    square = '[', ']',


class FormatSettings:
    str_len: int
    h_separator: str
    p_separator: str
    a_has_link: bool
    link_brackets: Brackets

    def __init__(self, str_len: int = 80, h_separator: str = '\n\n', p_separator: str = '\n\n', a_has_link: bool = True,
                 link_brackets: Brackets = Brackets.square):
        self.str_len = str_len
        self.h_separator = h_separator
        self.p_separator = p_separator
        self.a_has_link = a_has_link
        self.link_brackets = link_brackets

    def to_json(self):
        with open('to_docx_formatter.json', "w") as f:
            json.dump(self, f, default=lambda o: o.json(), indent=2)
        return json.dumps(self, default=lambda o: o.json(),
                          indent=2)

    def json(self):
        return {
            'str_len': self.str_len,
            'h_separator': self.h_separator,
            'p_separator': self.p_separator,
            'a_has_link': self.a_has_link,
            'link_brackets': self.link_brackets.name,
        }

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return cls(json_data['str_len'], json_data['h_separator'],
                   json_data['p_separator'], json_data['a_has_link'],
                   Brackets[json_data['link_brackets']])


class DocxSettings(FormatSettings):
    font_size: int = 14
    font: str = 'Arial'

    def __init__(self, font_size: int = 14, font: str = 'Arial', str_len: int = 80,
                 h_separator: str = '\n\n', p_separator: str = '\n\n', a_has_link: bool = True,
                 link_brackets: Brackets = Brackets.square):
        super().__init__(str_len, h_separator, p_separator, a_has_link, link_brackets)
        self.font_size = font_size
        self.font = font

    def json(self):
        return {
            **super().json(),
            'font_size': self.font_size,
            'font': self.font,
        }

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return cls(json_data['font_size'], json_data['font'], json_data['str_len'], json_data['h_separator'],
                   json_data['p_separator'], json_data['a_has_link'], Brackets[json_data['link_brackets']])
