import os

from app.ArticleParser.Formatters.FormatSettings import FormatSettings, DocxSettings
from app.ArticleParser.PageGetter import PageGetter
from app.ArticleParser.ArticleParcer import ArticleParser
from app.ArticleParser.Formatters.ToTxtFormatter import ToTxtFormatter
from app.ArticleParser.Formatters.ToDocxFormatter import ToDocxFormatter
from app.configs.Settings import Settings

settings = Settings()


def get_formatter():
    while True:
        extension = input("Введите формат сохранения: docx | txt. Чтобы выйти введите exit.")
        match extension:
            case 'txt':
                if settings.txt_settings_path and os.path.exists(settings.txt_settings_path):
                    s = FormatSettings.from_json(settings.txt_settings_path)
                    return ToTxtFormatter(s)
                return ToTxtFormatter()
            case 'docx':
                if settings.docx_settings_path and os.path.exists(settings.docx_settings_path):
                    s = DocxSettings.from_json(settings.txt_settings_path)
                    return ToDocxFormatter(s)
                return ToDocxFormatter()


def get_path(url):
    url = PageGetter.cut_url(url)
    idx = url.rfind('/')
    if idx == -1:
        filename = ''
    else:
        filename = url[idx+1:]
        url = url[:idx]
    path = os.path.join(settings.cur_dir, url)
    if not os.path.exists(path):
        os.makedirs(path)
    return {
        'path': path,
        'filename': filename,
    }


if __name__ == '__main__':
    while True:
        print('Добро пожаловать! Чтобы выйти введите exit.')
        url = input("Введите url: ")

        page = PageGetter.get_page(url)

        contents = ArticleParser.parse_html(page)
        if not contents:
            print('Ошибка! Не удалось получить страницу')
            continue

        formatter = get_formatter()
        formatter.format_contents(contents)

        full_path = get_path(url)
        formatter.save_file(full_path['path'], full_path['filename'])
