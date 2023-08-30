import os


class Config:
    def __init__(self):
        self.whisper_path = os.environ["WHISPER_PATH"]


CONFIG = Config()


def get_config():
    return CONFIG
