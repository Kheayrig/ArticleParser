import re

import requests


class PageGetter:
    """ Получает страницу по url
    """
    @staticmethod
    def get_page(url: str):
        """
        Получает страницу по url через response
        :param url: адрес страницы
        :return: html
        """
        response = requests.get(url)
        return response.content.decode('utf-8')

    @staticmethod
    def cut_url(url: str):
        """
        Обрезает url (удаляет https:/ или http:/, а также слэш, если он является концом строки)
        :param url: адрес страницы
        :return: url в формате site.com/page
        """
        if url[-1] == '/':
            url = url[:-1]
        if re.match('https:/.+', url):
            return url[8:]
        else:
            return url[7:]