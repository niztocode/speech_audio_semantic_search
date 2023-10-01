import os


class WeaviateConfig:
    def __init__(self):
        self.db_url = os.environ["WEAVIATE_DB_URL"]


WEAVIATE_CONFIG = WeaviateConfig()


def get_weaviate_config():
    return WEAVIATE_CONFIG