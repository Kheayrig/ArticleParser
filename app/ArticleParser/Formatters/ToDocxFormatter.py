import os
import re

from bs4 import NavigableString
from docx import Document
from docx.shared import Pt, Cm

from app.ArticleParser.Formatters.FormatSettings import DocxSettings


class ToDocxFormatter:

    def __init__(self, settings=DocxSettings()):
        self.document = Document()
        self.settings = settings
        style = self.document.styles['Normal']
        style.font.name = settings.font
        self.font_size = settings.font_size
        style.font.size = Pt(self.font_size)
        self.paragraph_len = self.convert_symbols_to_cm()

    def convert_symbols_to_cm(self):
        return Cm((self.settings.str_len * self.font_size) / 28.3465)

    def save_file(self, path, filename) -> str:
        full_path = os.path.join(path, f'{filename}.docx')
        self.document.save(full_path)
        return full_path

    def format_contents(self, contents: list):
        for i in range(len(contents)):
            p = self.document.add_paragraph()
            match contents[i].name:
                case 'div' | 'span' | 'p':
                    p.width = self.paragraph_len
                    children = contents[i].contents
                    self.format_children(children, p)
                    p.add_run(self.settings.p_separator)
                case _:
                    self.format_tag(contents[i], p)
        return self.document

    def format_children(self, contents: list, p) -> None:
        for j in range(len(contents)):
            if isinstance(contents[j], NavigableString):
                p.add_run(contents[j].text)
                p.add_run(' ')
                continue
            self.format_tag(contents[j], p)

    def format_tag(self, tag, p):
        match tag.name:
            case 'ul' | 'ol':
                self.ul(tag)
            case 'h1':
                self.h(tag, 6, p)
            case 'h2':
                self.h(tag, 4, p)
            case 'h3':
                self.h(tag, 2, p)
            case 'a':
                self.a(tag, p)
            case 'b' | 'strong':
                self.b(tag, p)
            case 'i' | 'em':
                self.i(tag, p)
            case 'u' | 'ins':
                self.u(tag, p)
            case 's' | 'del':
                self.s(tag, p)
            case 'sub':
                self.sub(tag, p)
            case 'sup':
                self.sup(tag, p)
            case 'br':
                p.add_run('\n')
            case _:
                p.add_run(tag.text)
                p.add_run(' ')

    def a(self, tag, p):
        href = tag.get('href')
        if not self.settings.a_has_link or href is None:
            p.add_run(f'{tag.text} ')
        else:
            p.add_run(
                f"{tag.text} {self.settings.link_brackets.value[0]}{href}{self.settings.link_brackets.value[-1]}")

    def b(self, tag, p):
        p.add_run(tag.text).font.bold = True

    def i(self, tag, p):
        p.add_run(tag.text).font.italic = True

    def u(self, tag, p):
        p.add_run(tag.text).font.underline = True

    def s(self, tag, p):
        p.add_run(tag.text).font.strike = True

    def ul(self, tag):
        contents = tag.contents
        for li in contents:
            self.li(li)
        self.document.add_paragraph().width = self.paragraph_len

    def sub(self, tag, p):
        p.add_run(tag.text).font.subscript = True

    def sup(self, tag, p):
        p.add_run(tag.text).font.superscript = True

    def li(self, tag):
        if re.match('\s+', tag.text):
            return
        p = self.document.add_paragraph('• ')
        p.width = self.paragraph_len
        if isinstance(tag, NavigableString):
            p.add_run(tag.text)
            return
        children = tag.contents
        for item in children:
            self.format_tag(item, p)
        p.add_run('\n')

    def h(self, tag, size_plus, p) -> None:
        text = f'{tag.text}{self.settings.h_separator}'
        h = p.add_run(text)
        h.bold = True
        h.font.size = Pt(self.font_size + size_plus)
