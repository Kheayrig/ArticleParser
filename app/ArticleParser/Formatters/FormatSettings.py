import json
from enum import Enum


class Brackets(Enum):
    """
    Перечисление скобок для оформления адреса ссылки.
    Brackets.value[0] - открывающая скобка,
    Brackets.value[1] - закрывающая скобка

            Attributes:
                none: отсутствие скобок = '', '',
                round: круглые скобки = '(', ')',
                square: квадратные скобки = '[', ']',
    """
    none = '', '',
    round = '(', ')',
    square = '[', ']',


class FormatSettings:
    """ Настройки txt файла

            Attributes:
                str_len (int): длина строки в симолах = 80
                h_separator (str): разделитель строки для заголовков = '\n\n'
                p_separator (str): разделитель строки для абзацев = '\n\n'
                a_has_link (bool): нужно ли печатать адрес ссылки = False
                link_brackets (Brackets): скобки, которыми оформляется ссылка = Brackets.square
    """
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
        """
        Сериализует класс
        :return: json str
        """
        return json.dumps(self, default=lambda o: o.json(), indent=2)

    def json(self):
        """
        dict аттрибутов для сериализации
        :return: dict
        """
        return {
            'str_len': self.str_len,
            'h_separator': self.h_separator,
            'p_separator': self.p_separator,
            'a_has_link': self.a_has_link,
            'link_brackets': self.link_brackets.name,
        }

    @classmethod
    def from_json(cls, filepath):
        """
        Десереализует класс
        :param filepath: путь, по которому лежит json
        :return: FormatSettings()
        """
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return cls(json_data['str_len'], json_data['h_separator'],
                   json_data['p_separator'], json_data['a_has_link'],
                   Brackets[json_data['link_brackets']])


class DocxSettings(FormatSettings):
    """ Настройки docx файла

                Attributes:
                    font_size (int): размер шрифта = 14
                    font (str): шрифт = 'Arial'
        """
    font_size: int = 14
    font: str = 'Arial'

    def __init__(self, font_size: int = 14, font: str = 'Arial', str_len: int = 80,
                 h_separator: str = '\n\n', p_separator: str = '\n\n', a_has_link: bool = True,
                 link_brackets: Brackets = Brackets.square):
        super().__init__(str_len, h_separator, p_separator, a_has_link, link_brackets)
        self.font_size = font_size
        self.font = font

    def json(self):
        """
                dict аттрибутов для сериализации
                :return: dict
                """
        return {
            **super().json(),
            'font_size': self.font_size,
            'font': self.font,
        }

    @classmethod
    def from_json(cls, filepath):
        """
                Десереализует класс
                :param filepath: путь, по которому лежит json
                :return: FormatSettings()
                """
        with open(filepath, "r") as f:
            json_data = json.load(f)
        return cls(json_data['font_size'], json_data['font'], json_data['str_len'], json_data['h_separator'],
                   json_data['p_separator'], json_data['a_has_link'], Brackets[json_data['link_brackets']])
