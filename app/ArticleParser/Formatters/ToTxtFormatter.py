import os.path
import re
import textwrap

from bs4 import Tag, NavigableString

from app.ArticleParser.Formatters.FormatSettings import FormatSettings


class ToTxtFormatter:
    """ Преобразует теги html в документ .txt

                    Attributes:
                        document (Document): документ - list[str]
                        settings (DocxSettings): файл настроек
            """

    def __init__(self, settings=FormatSettings()):
        self.document = []
        self.settings = settings

    def save_file(self, path: str, filename: str, ) -> str:
        """
                Сохраняет self.document
                :param path: путь к директории файла
                :param filename: имя файла
                :return: full_path - полный путь
                """
        full_path = os.path.join(path, f'{filename}.txt')
        with open(full_path, 'w', encoding="utf-8") as output_file:
            output_file.write(''.join(self.document))
        return full_path

    def format_contents(self, contents: list) -> list:
        """
                Проходит по тегам, создаёт параграфы
                :param contents: теги
                :return: list
                """
        for i in range(len(contents)):
            children = contents[i].contents
            self.format_children(children)
            contents[i].string = ''.join(children)
            self.add_paragraph(contents[i])
        return self.document

    def format_children(self, contents: list) -> None:
        """
                Проходит по дочерним элементам тега: вызывает метод класса по названию тега и рекурсивно форматирует строку
                :param contents: список Tag | NavigableString
                :param p: текущий абзац
                :return: None
                """
        for j in range(len(contents)):
            if not isinstance(contents[j], NavigableString):
                children = contents[j].contents
                if len(children) > 1:
                    self.format_children(children)
            contents[j].replace_with(self.format_tag(contents[j]))

    def format_tag(self, tag: Tag | NavigableString) -> str:
        """
                Определяет тег по названию и вызывает соответствующий метод класс, иначе возвращает текст тега
                :param tag: тег
                :param p: текущий абзац
                :return: str
                """
        if isinstance(tag, NavigableString):
            return re.sub(r' +', ' ', f'{tag.text} ')

        match tag.name:
            case 'a':
                return self.a(tag)
            case 'sub':
                return self.sub(tag)
            case 'sup':
                return self.sup(tag)
            case 'li':
                return self.li(tag)
            case 'h1' | 'h2' | 'h3':
                return self.h(tag)
            case 'br':
                return '\n'
            case _:
                return re.sub(r' +', ' ', f'{tag.text} ')

    def add_paragraph(self, tag: Tag) -> None:
        """
        Добавляет в self.document и форматирует абзац(по ширине строки в символах)
        :param tag: тег
        :return: None
        """
        text = re.sub(r'\s{3,}', self.settings.p_separator, tag.text)
        if len(text) <= self.settings.str_len:
            self.document.append(text)
        else:
            text = textwrap.wrap(text, self.settings.str_len, break_long_words=False, replace_whitespace=False)
            self.document.append('\n'.join(text))
        self.document.append(self.settings.p_separator)

    def a(self, tag) -> str:
        href = tag.get('href')
        if not self.settings.a_has_link or href is None:
            return f'{tag.text} '
        return f"{tag.text} {self.settings.link_brackets.value[0]}{href}{self.settings.link_brackets.value[-1]} "

    def sub(self, tag) -> str:
        return f'(_{tag.text}) '

    def sup(self, tag) -> str:
        return f'^({tag.text}) '

    def li(self, tag) -> str:
        text = re.sub(r'^[\r\n]+', '', tag.text)
        return f" • {text} "

    def h(self, tag) -> str:
        return f'{tag.text}{self.settings.h_separator}'
