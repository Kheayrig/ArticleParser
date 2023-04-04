import os
from dotenv import load_dotenv


class Settings:
    cur_dir: str = None
    txt_settings_path: str = None
    docx_settings_path: str = None

    def __init__(self):
        load_dotenv(verbose=True)
        self.cur_dir = os.getenv('CUR_DIR')
        if self.cur_dir is None:
            self.cur_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '..')), 'tests')
            if not os.path.exists(self.cur_dir):
                os.makedirs(self.cur_dir)
        self.txt_settings_path = os.getenv('TXT_SETTINGS_PATH')
        self.docx_settings_path = os.getenv('DOCX_SETTINGS_PATH')
