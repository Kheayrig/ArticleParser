import re

import requests


class PageGetter:
    @staticmethod
    def get_page(url: str):
        response = requests.get(url)
        return response.content.decode('utf-8')

    @staticmethod
    def cut_url(url: str):
        if url[-1] == '/':
            url = url[:-1]
        if re.match('https:/.+', url):
            return url[8:]
        else:
            return url[7:]