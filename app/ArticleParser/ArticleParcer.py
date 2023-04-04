from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re


class ArticleParser:
    black_tags_list = ['head', 'nav', 'aside', 'script', 'a', 'header', 'footer', 'figure', 'svg', 'style',
                       'img', 'form']
    white_tags_list = ['div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul']
    black_classes_list = re.compile(r".*footer.*|^header.*|.*btn.*|.*button.*|.*hide.*|.*hidden.*|.*meta.*")

    @staticmethod
    def parse_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all():
            if tag.name is None:
                continue
            if tag.name in ArticleParser.black_tags_list:
                if tag.name == 'a' and ArticleParser.check_tag(tag.parent):
                    continue
                tag.decompose()
            elif tag.get('class') and re.match(ArticleParser.black_classes_list, tag.get('class')[0]):
                tag.decompose()
        res = []
        for tag in soup.find_all(ArticleParser.white_tags_list):
            ArticleParser.span_to_h_replace(tag)
            if ArticleParser.check_tag(tag):
                res.append(tag)
        return res

    @staticmethod
    def check_tag(tag) -> bool:
        if not ArticleParser.filter_tag_text(tag):
            return False
        children = tag.contents
        for child in children:
            if isinstance(child, NavigableString) and ArticleParser.filter_tag_text(child):
                return True
        return False

    @staticmethod
    def filter_tag_text(tag):
        if re.match(r'^[\s\n\t]*$', tag.text):
            return False
        return True

    @staticmethod
    def span_to_h_replace(tag):
        parent = tag.find_parent(re.compile('^h\d+'))
        if parent is not None:
            tag.name = parent.name
            parent.replace_with(tag)

