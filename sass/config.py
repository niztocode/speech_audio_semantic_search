import os


class AppConfig:
    def __init__(self):
        self.library_path = os.environ["LIBRARY_PATH"]


CONFIG = AppConfig()


def get_app_config():
    return CONFIG
