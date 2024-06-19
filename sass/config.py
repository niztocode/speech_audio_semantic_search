import os


class AppConfig:
    def __init__(self):
        self.library_path = os.environ["LIBRARY_PATH"]
        self.huggingface_token = os.environ["HUGGINGFACE_TOKEN"]
        self.segmentation_model_path = os.environ["SEGMENTATION_MODEL_PATH"]
        self.diarization_pipeline_path = os.environ["DIARIZATION_PIPELINE_PATH"]


CONFIG = AppConfig()


def get_app_config():
    return CONFIG
