import os
from dotenv import load_dotenv


class Settings:
    """
    Класс с настройками программы

    Attributes:
        cur_dir (str): текущая директория, в которую будет сохранён файл (ВАЖНО: будут созданы поддиректории по пути файла)
        txt_settings_path (str): optional : Путь к файлу настроек для ToTxtFormatter
        docx_settings_path (str): optional : Путь к файлу настроек для ToDocxFormatter
    """
    cur_dir: str = None
    txt_settings_path: str = None
    docx_settings_path: str = None

    def __init__(self):
        """
        Получает переменные окружения из .env, иначе создаёт папку test в articleParse для сохранения файлов
        """
        load_dotenv(verbose=True)
        self.cur_dir = os.getenv('CUR_DIR')
        if self.cur_dir is None:
            self.cur_dir = os.path.join(os.path.join(os.getcwd(), 'tests'))
            if not os.path.exists(self.cur_dir):
                os.makedirs(self.cur_dir)
        self.txt_settings_path = os.getenv('TXT_SETTINGS_PATH')
        self.docx_settings_path = os.getenv('DOCX_SETTINGS_PATH')
